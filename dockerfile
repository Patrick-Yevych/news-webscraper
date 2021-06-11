FROM python:latest
RUN pip install beautifulsoup4
RUN pip install pandas
CMD ["python", "ScraperApp.py"]
COPY Scraper.py /Scraper.py
COPY GoogleScraper.py /GoogleScraper.py 
COPY ScraperApp.py /ScraperApp.py
