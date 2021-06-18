import json, mysql.connector, datetime
import pandas as pd

class DatabaseConnection():

    cfg = None
    db_con = None
    cs = None

    def __init__(self, cfg_dir: str):
        self.cfg = json.load(open(cfg_dir,))
        self.db_con = mysql.connector.connect(host=self.cfg['db_con']['host'], user=self.cfg['db_con']['user'], password=self.cfg['db_con']['password'], database=self.cfg['db_con']['database'])
        self.db_con.autocommit = True
        self.cs = self.db_con.cursor(prepared=True)

    def res_insert(self, scraper: dict, results: pd.DataFrame) -> None:
        for row in results.values.tolist():
            STMT = "INSERT INTO Results(headline, source, url, published_date, search_query, engine) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url=%s, published_date=%s, search_query=%s, engine=%s;" 
            date = datetime.datetime.strptime(row[3], '%a %b %d %Y')
            self.cs.execute(STMT, (row[0], row[1], row[2], date, scraper['search_query'], scraper['engine'], row[2], date, scraper['search_query'], scraper['engine']))

    def scraper_insert(self, scraper: dict) -> None:
        STMT = "INSERT INTO Scrapers(search_query, engine, max_pages, page_step) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE max_pages=%s, page_step=%s;"
        self.cs.execute(STMT, (scraper['search_query'], scraper['engine'], scraper['max_pages'], scraper['page_step'], scraper['max_pages'], scraper['page_step']))

    def res_selectall(self) -> list:
        res = []
        STMT = "SELECT * FROM Results;"
        self.cs.execute(STMT)
        for headline, source, url, published_date, search_query, engine in self.cs:
            res.append({"headline": headline, "source": source, "url": url, "published_date": published_date, "search_query": search_query, "engine": engine})
        return res

    def scraper_selectall(self) -> list:
        res = []
        STMT = "SELECT * FROM Scrapers;"
        self.cs.execute(STMT)
        for search_query, engine, max_pages, page_step in self.cs:
            res.append({"search_query": search_query, "engine": engine, "max_pages": max_pages, "page_step": page_step})
        return res

    def destroy(self) -> None:
        self.cs.close()
        self.db_con.close()