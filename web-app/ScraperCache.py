from threading import Timer
from DatabaseConnection import DatabaseConnection
from GoogleScraper import GoogleScraper
import _thread, datetime

class ScraperCache:
    cache = None
    timer = None

    def push(self, key: tuple, interval_value: int, interval_metric: str) -> None:
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

        self.cache[key] = {"running": True, "countdown": c*interval_value, "interval": c*interval_value}
        print(self.cache)

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

    def pause(self, key: tuple) -> None:
        self.cache[key]['running'] = False

    def unpause(self, key: tuple) -> None:
        self.cache[key]['running'] = True

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
        for scraper in db.scraper_selectall():
            if (scraper["run_interval_metric"] != 'manual'):
                self.push((scraper["search_query"], scraper["engine"]), scraper["run_interval_value"], scraper["run_interval_metric"])
        db.destroy()

    def tick(self) -> dict:
        print(self.cache)
        for k in self.cache:
            if (self.cache[k]['running'] == True):
                self.cache[k]['countdown'] -= 1
                if (self.cache[k]['countdown'] <= 0):
                    self.cache[k]['countdown'] = self.cache[k]['interval']
                    print("Starting ", k)
                    _thread.start_new_thread(self.scrape, (k,))

    def __init__(self):
        self.cache = {}
        self.load()
        self.timer = Timer(60, self.tick)
        self.timer.start()