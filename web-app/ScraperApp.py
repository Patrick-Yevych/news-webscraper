import mysql.connector
#sys.path.append('../')
from GoogleScraper import GoogleScraper
from DatabaseConnection import DatabaseConnection

USE_JSON = False

if __name__ == '__main__':

    db = DatabaseConnection("./config.json")

    for scraper in (db.scraper_selectall(), db.cfg['scrapers'])[USE_JSON]:
        print (scraper)
        if scraper['engine'].lower() == 'google':
            s = GoogleScraper(scraper['search_query'], scraper['max_pages'], scraper['page_step'])
            t = s.build_table()
            db.res_insert(scraper, t)

    db.destroy()