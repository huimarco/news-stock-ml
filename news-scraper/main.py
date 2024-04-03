import datetime
from scrapers import scrape_wsj

if __name__ == "__main__":
    start_date = datetime.date(2024, 3, 29)
    end_date = datetime.date(2024, 3, 31)
    wsj = scrape_wsj(start_date, end_date)
    print(len(wsj))
    print(wsj.head(5))