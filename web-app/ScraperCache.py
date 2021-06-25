from threading import Timer

class ScraperCache:
    cache = None
    timer = None

    def push(self, key: tuple, interval_value: int, interval_metric: str) -> None:
        c = 0
        if interval_metric == "minute":
            c = 60
        elif interval_metric == "hour":
            c = 60*60
        elif interval_metric == "day":
            c = 24*60*60
        elif interval_metric == "month":
            c = 30*24*60*60
        elif interval_metric == "year":
            c = 12*30*24*60*60

        self.cache[key] = {"running": True, "countdown": c*interval_value, "interval": c*interval_value}

    def pop(self, key: tuple) -> None:
        self.cache.pop(key)

    def pause(self, key: tuple) -> None:
        self.cache[key]['running'] = False

    def unpause(self, key: tuple) -> None:
        self.cache[key]['running'] = True

    def tick(self) -> dict:
        res = []
        for k, v in self.cache:
            if (v['running'] == True):
                v['countdown'] -= 1
                if (v['countdown'] <= 0):
                    res.append(k)
                    v['countdown'] = v['interval']
        return res

    def __init__(self):
        self.cache = {}
        self.timer = Timer(60, self.tick)
        self.timer.start()