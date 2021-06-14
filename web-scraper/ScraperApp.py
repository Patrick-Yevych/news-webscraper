import pandas
from GoogleScraper import GoogleScraper
import json, mysql.connector, datetime
import pandas as pd

def res_insert(scraper, results: pd.DataFrame, cursor) -> None:
    for row in results.values.tolist():
        #stmt = "INSERT INTO Results(headline, source, url, published_date, search_query, engine) VALUES (" \
                        #+row[0]+", "+row[1]+", "+row[2]+", "+row[3]+", "+scraper['query']+", "+scraper['engine']+" );"
        stmt = "INSERT INTO Results(headline, source, url, published_date, search_query, engine) VALUES ( %s, %s, %s, %s, %s, %s);" 
        date = datetime.datetime.strptime(row[3], '%a %b %d %Y')
        cursor.execute(stmt, (row[0], row[1], row[2], date, scraper['query'], scraper['engine']))

def scraper_insert(scraper, cursor) -> None:
    stmt = "INSERT INTO Scrapers(search_query, engine, max_pages, page_step) VALUES (%s, %s, %s, %s);"
    cursor.execute(stmt, (scraper['query'], scraper['engine'], scraper['max_pages'], scraper['page_step']))

if __name__ == '__main__':
    cfg = json.load(open('config.json',))
    print(cfg['db_con'])
    db_con = mysql.connector.connect(host=cfg['db_con']['host'], user=cfg['db_con']['user'], password=cfg['db_con']['password'], database=cfg['db_con']['database'])
    cs = db_con.cursor(prepared=True)

    for scraper in cfg['scrapers']:
        #scraper_insert(scraper, cs)
        if scraper['engine'].lower() == 'google':
            s = GoogleScraper(scraper['query'], scraper['max_pages'], scraper['page_step'])
            t = s.build_table()
            res_insert(scraper, t, cs)