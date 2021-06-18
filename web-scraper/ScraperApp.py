from GoogleScraper import GoogleScraper
import json, mysql.connector, datetime
import pandas as pd

USE_JSON = False

def res_insert(scraper: dict, results: pd.DataFrame, cursor) -> None:
    for row in results.values.tolist():
        STMT = "INSERT INTO Results(headline, source, url, published_date, search_query, engine) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE headline=%s, source=%s;" 
        date = datetime.datetime.strptime(row[3], '%a %b %d %Y')
        cursor.execute(STMT, (row[0], row[1], row[2], date, scraper['search_query'], scraper['engine'], row[0], row[1]))

def scraper_insert(scraper: dict, cursor) -> None:
    STMT = "INSERT INTO Scrapers(search_query, engine, max_pages, page_step) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE search_query=%s, engine=%s;"
    cursor.execute(STMT, (scraper['search_query'], scraper['engine'], scraper['max_pages'], scraper['page_step'], scraper['search_query'], scraper['engine']))

def scraper_selectall(cursor) -> dict:
    res = []
    STMT = "SELECT * FROM Scrapers;"
    cursor.execute(STMT)
    for search_query, engine, max_pages, page_step in cursor:
        res.append({"search_query": search_query, "engine": engine, "max_pages": max_pages, "page_step": page_step})
    return res

if __name__ == '__main__':
    cfg = json.load(open('../config.json',))
    db_con = mysql.connector.connect(host=cfg['db_con']['host'], user=cfg['db_con']['user'], password=cfg['db_con']['password'], database=cfg['db_con']['database'])
    db_con.autocommit = True
    cs = db_con.cursor(prepared=True)

    for scraper in (scraper_selectall(cs), cfg['scrapers'])[USE_JSON]:
        print (scraper)
        try:
            if scraper['engine'].lower() == 'google':
                s = GoogleScraper(scraper['search_query'], scraper['max_pages'], scraper['page_step'])
                t = s.build_table()
                res_insert(scraper, t, cs)
        except mysql.connector.errors.InterfaceError as e:
            print(e)

    cs.close()
    db_con.close()