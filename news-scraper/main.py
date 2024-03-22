import datetime
from scrapers import scrape_wsj

if __name__ == "__main__":
    start_date = datetime.date(2023, 3, 19)
    end_date = datetime.date(2023, 3, 21)
    wsj = scrape_wsj(start_date, end_date)
    print(wsj.head(10))