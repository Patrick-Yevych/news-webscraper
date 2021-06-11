from GoogleScraper import GoogleScraper
import json


if __name__ == '__main__':
    cfg = json.load(open('config.json',))
    for scraper in cfg['scrapers']:
        if scraper['site'].lower() == 'google':
            s = GoogleScraper(scraper['query'], scraper['max_results'], scraper['per_page'])
            t = s.build_table()
            t.to_csv(scraper['query']+'.csv')
            print(t)
