from DatabaseConnection import DatabaseConnection
from GoogleScraper import GoogleScraper
import _thread, datetime, math, time

class ScraperCache:
    cache = None

    def push(self, key: tuple, interval_value: int, interval_metric: str, running: bool) -> None:
        c = 0
        if interval_metric == "minute":
            c = 1
        elif interval_metric == "hour":
            c = 60
        elif interval_metric == "day":
            c = 24*60
        elif interval_metric == "month":
            c = 30*24*60
        elif interval_metric == "year":
            c = 12*30*24*60

        if (running == None):
            running = False

        if (interval_value > 0 and interval_value % math.floor(interval_value) == 0 and interval_metric != 'manual'):
            if (key not in self.cache):
                self.cache[key] = {"running": running, "countdown": c*interval_value, "interval": c*interval_value}
            else:
                self.cache[key] = {"running": running, "countdown": self.cache[key]['countdown'], "interval": c*interval_value}


    def pop(self, key: tuple) -> dict:
        try:
            res = self.cache.pop(key)
            return {key: res}
        except (KeyError):
            return None


    def get(self, key: tuple) -> dict:
        try:
            return self.cache[key]
        except (KeyError):
            return None


    def scrape(self, key: tuple) -> None:
        db = DatabaseConnection("./config.json")
        
        scraper = db.scraper_select(key[0], key[1])
        now = datetime.datetime.now()
        db.scraper_update_runtime(key[0], key[1], now.strftime('%Y-%m-%d %H:%M:%S'))
        
        if scraper['engine'].lower() == 'google':
            s = GoogleScraper(scraper['search_query'], scraper['max_pages'], scraper['page_step'], scraper['per_page'])
            db.res_insert({"search_query": scraper['search_query'], "engine": scraper['engine']}, s.build_table())

        db.destroy()


    def load(self) -> None:
        db = DatabaseConnection("./config.json")
        for scraper in db.scraper_select_autorun():
            self.push((scraper["search_query"], scraper["engine"]), scraper["run_interval_value"], scraper["run_interval_metric"], scraper['running'])
        db.destroy()


    def prune(self) -> None:
        db = DatabaseConnection("./config.json")
        try:
            for k in self.cache:
                if (db.scraper_select(k[0], k[1]) == None):
                    self.pop(k)
        except (RuntimeError):
            print("RuntimeError, re-attempting prune")
            self.prune()
        db.destroy()


    def dispatch(self) -> None:
        for k in self.cache:
            if (self.cache[k]['running'] == True):
                self.cache[k]['countdown'] -= 1
                if (self.cache[k]['countdown'] <= 0):
                    self.cache[k]['countdown'] = self.cache[k]['interval']
                    _thread.start_new_thread(self.scrape, (k,))


    def tick(self) -> None:
        self.load()
        self.prune()
        self.dispatch()
        print(self.cache)


    def __init__(self):
        self.cache = {}
        self.load()


if __name__ == '__main__':
    scraper_cache = ScraperCache()
    while True:
        scraper_cache.tick()
        time.sleep(60)