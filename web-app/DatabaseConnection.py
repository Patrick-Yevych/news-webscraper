import json, mysql.connector

from pandas.core.frame import DataFrame
import pandas as pd

"""
A database connector wrapper for res-database.
"""
class DatabaseConnection():

    cfg = None
    db_con = None
    cs = None

    def __init__(self, cfg_dir: str):
        self.cfg = json.load(open(cfg_dir,))
        self.db_con = mysql.connector.connect(host=self.cfg['db_con']['host'], user=self.cfg['db_con']['user'], password=self.cfg['db_con']['password'], database=self.cfg['db_con']['database'])
        self.db_con.autocommit = True
        self.cs = self.db_con.cursor(prepared=True)

    """
    Preconditions: 
    
    scraper is a dictionary containing the fields
    (headline, source, url, published_date, search_query, engine). 
    
    results is a dataframe with the columns
    ['Headline', 'Source', 'URL', 'Date'].
    
    Postconditions:

    Inserts the columns in the dataframe results into the results table of res_database with foreign key (search_query engine) referencing scrapers.
    Replaces duplicate record if exists.
    """
    def res_insert(self, scraper: dict, results: pd.DataFrame) -> None:
        for row in results.values.tolist():
            STMT = "INSERT INTO Results(headline, source, url, published_date, search_query, engine) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url=%s, published_date=%s, search_query=%s, engine=%s;" 

            self.cs.execute(STMT, (row[0], row[1], row[2], row[3], scraper['search_query'], 
                                   scraper['engine'], row[2], row[3], scraper['search_query'], 
                                   scraper['engine']))

    """
    Preconditions:

    scraper is a dictionary containing the fields
    (headline, source, url, published_date, search_query, engine).

    Postconditions:

    Inserts the scraper into the scrapers table of res_database. Replaces duplicate record if exists.
    """
    def scraper_insert(self, scraper: dict) -> None:
        STMT = "INSERT INTO Scrapers(search_query, engine, max_pages, page_step, per_page, run_interval_value, run_interval_metric) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE max_pages=%s, page_step=%s, per_page=%s, run_interval_value=%s, run_interval_metric=%s;"

        self.cs.execute(STMT, (scraper['search_query'], scraper['engine'], scraper['max_pages'], 
                               scraper['page_step'], scraper['per_page'], scraper['run_interval_value'], 
                               scraper['run_interval_metric'], scraper['max_pages'], scraper['page_step'], 
                               scraper['per_page'], scraper['run_interval_value'], scraper['run_interval_metric']))

    """
    Preconditions:

    runtime is a datetime string format as '%Y-%m-%d %H:%M:%S'.

    Postconditions:

    Updates the last_run field of the scraper with key (search_query, engine)
    to runtime.
    """
    def scraper_update_runtime(self, search_query: str, engine: str, runtime) -> None:
        STMT = "UPDATE Scrapers SET last_run=%s WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (runtime, search_query, engine))
        
    """
    Postconditions:

    Retrieve all records from the results table of res_database
    as a list of dictionaries.
    """
    def res_selectall(self) -> list:
        res = []
        STMT = "SELECT * FROM Results;"
        self.cs.execute(STMT)
        for headline, source, url, published_date, search_query, engine in self.cs:
            res.append({"headline": headline, "source": source, "url": url, "published_date": published_date, "search_query": search_query, "engine": engine})
        return res

    """
    Postconditions:

    Retrieve all records from the scrapers table of res_database
    as a list of dictionaries.
    """
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

    """
    Postconditions:

    Retrieve the record with the matching primary key (headline, source)
    as a dictionary.
    """
    def res_select(self, headline: str, source: str) -> dict:
        STMT = "SELECT * FROM Results WHERE headline=%s AND source=%s;"
        self.cs.execute(STMT, (headline, source))
        for headline, source, url, published_date, search_query, engine in self.cs:
            return {"headline": headline, "source": source, "url": url, 
                    "published_date": published_date, "search_query": search_query, "engine": engine}

    """
    Postconditions:

    Retrieve all records with the matching foreign key (search_query, engine)
    referencing the scrapers table as a list of dictionaries.
    """
    def res_foreign_select(self, search_query: str, engine: str) -> list:
        res = []
        STMT = "SELECT * FROM Results WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (search_query, engine))
        for headline, source, url, published_date, search_query, engine in self.cs:
            res.append({"headline": headline, "source": source, "url": url, "published_date": published_date, "search_query": search_query, "engine": engine})
        return res

    """
    Postconditions:

    Retrieve the scraper with the matching primary key (search_query, engine)
    as a dictionary.
    """
    def scraper_select(self, search_query: str, engine: str) -> dict:
        STMT = "SELECT * FROM Scrapers WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (search_query, engine))
        for search_query, engine, max_pages, page_step, per_page, run_interval_value, run_interval_metric, last_run in self.cs:

            return {"search_query": search_query, "engine": engine, 
                        "max_pages": max_pages, "page_step": page_step, 
                        "per_page": per_page, "run_interval_value": run_interval_value,
                        "run_interval_metric": run_interval_metric, "last_run": last_run}

    """
    Postconditions:

    Delete the record with the matching primary key (search_query, engine).
    """
    def scraper_delete(self, search_query: str, engine: str):
        STMT = "DELETE FROM Scrapers WHERE search_query=%s AND engine=%s;"
        self.cs.execute(STMT, (search_query, engine))

    """
    Postconditions:

    Delete the record with the matching primary key (headline, source).
    """
    def result_delete(self, headline: str, source: str):
        STMT = "DELETE FROM Results WHERE headline=%s AND source=%s"
        self.cs.execute(STMT, (headline, source))

    """
    Postconditions:

    Return a dictionary counting the number of records with the given primary (search_query, engine)
    grouped by their sources.
    """
    def sources_count(self, search_query: str, engine: str) -> dict:
        res = {}
        STMT = "SELECT source, COUNT(source) as num_posts FROM Results WHERE search_query=%s AND engine=%s GROUP BY source;"
        self.cs.execute(STMT, (search_query, engine))
        for source, num_posts in self.cs:
            res[source] = num_posts
        return res

    def destroy(self) -> None:
        self.cs.close()
        self.db_con.close()