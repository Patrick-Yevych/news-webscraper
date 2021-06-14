from GoogleScraper import GoogleScraper
import json, mysql.connector


if __name__ == '__main__':
    cfg = json.load(open('config.json',))
    print(cfg['db_con'])
    db_con = mysql.connector.connect(host=cfg['db_con']['host'], user=cfg['db_con']['user'], password=cfg['db_con']['password'], database=cfg['db_con']['database'])

    for scraper in cfg['scrapers']:
        if scraper['engine'].lower() == 'google':
            s = GoogleScraper(scraper['query'], scraper['max_pages'], scraper['page_step'])
            t = s.build_table()
