import json, mysql.connector
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

            self.cs.execute(STMT, (row[0], row[1], row[2], row[3], scraper['search_query'], 
                                   scraper['engine'], row[2], row[3], scraper['search_query'], 
                                   scraper['engine']))

    def scraper_insert(self, scraper: dict) -> None:
        STMT = "INSERT INTO Scrapers(search_query, engine, max_pages, page_step, per_page, run_interval_value, run_interval_metric) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE max_pages=%s, page_step=%s, per_page=%s, run_interval_value=%s, run_interval_metric=%s;"

        self.cs.execute(STMT, (scraper['search_query'], scraper['engine'], scraper['max_pages'], 
                               scraper['page_step'], scraper['per_page'], scraper['run_interval_value'], 
                               scraper['run_interval_metric'], scraper['max_pages'], scraper['page_step'], 
                               scraper['per_page'], scraper['run_interval_value'], scraper['run_interval_metric']))

    def res_selectall(self) -> dict:
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
        for search_query, engine, max_pages, page_step, per_page, run_interval_value, run_interval_metric, last_run in self.cs:

            res.append({"search_query": search_query, "engine": engine, 
                        "max_pages": max_pages, "page_step": page_step, 
                        "per_page": per_page, "run_interval_value": run_interval_value,
                        "run_interval_metric": run_interval_metric, "last_run": last_run})

        return res

    def scraper_select(self, search_query: str, engine: str) -> dict:
        STMT = "SELECT * FROM Scrapers WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (search_query, engine))
        for search_query, engine, max_pages, page_step, per_page, run_interval_value, run_interval_metric, last_run in self.cs:

            return {"search_query": search_query, "engine": engine, 
                        "max_pages": max_pages, "page_step": page_step, 
                        "per_page": per_page, "run_interval_value": run_interval_value,
                        "run_interval_metric": run_interval_metric, "last_run": last_run}

    def scraper_delete(self, search_query: str, engine: str):
        STMT = "DELETE FROM Scrapers WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (search_query, engine))

    def result_delete(self, headline: str, source: str):
        STMT = "DELETE FROM Results WHERE headline=%s AND source=%s"
        self.cs.execute(STMT, (headline, source))

    def destroy(self) -> None:
        self.cs.close()
        self.db_con.close()