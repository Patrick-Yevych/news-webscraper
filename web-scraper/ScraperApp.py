from GoogleScraper import GoogleScraper
import json


if __name__ == '__main__':
    cfg = json.load(open('config.json',))
    for scraper in cfg['scrapers']:
        if scraper['engine'].lower() == 'google':
            s = GoogleScraper(scraper['query'], scraper['max_pages'], scraper['page_step'])
            t = s.build_table()
            t.to_csv(scraper['query']+'.csv')
            print(t)
