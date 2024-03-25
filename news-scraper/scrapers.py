from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Function to scrape all headlines on WSJ on a given day
def scrape_wsj_date(driver, date):
    # Base URL
    base_url = f'https://www.wsj.com/news/archive/{str(date.year)}/{str(date.month).zfill(2)}/{str(date.day).zfill(2)}?page='

    # Initialize lists to store data
    all_articles = []

    # Create page counter
    page_num = 1

    # Loop through each page
    while True:
        # URL of the webpage to scrape
        url = base_url + str(page_num)

        # Open the webpage
        driver.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all articles on the page
        articles = soup.find_all('article')

        # Exit loop if no more articles on page
        if not articles: 
            break
        
        all_articles.append(articles)
        
        # Increment page
        page_num += 1

    return all_articles

def scrape_wsj(start_date, end_date):
    # Start a WebDriver (you need to have chromedriver installed in your system and its path added to the environment variables)
    driver = webdriver.Edge()

    # Generate a list of DataFrames for each day
    all_articles = [scrape_wsj_date(driver, current_date) for current_date in pd.date_range(start_date, end_date)]

    # Close the WebDriver
    driver.quit()
    
    return all_articles

def extract_wsj_date(articles):
    # Initialize lists to store data
    topics = []
    headlines = []
    published_times = []
    article_links = []

    # Extract data from each article
    for article in articles:
        # Extract topic
        topic = article.find('div', class_='WSJTheme--articleType--34Gt-vdG').text.strip()
        topics.append(topic)
        
        # Extract headline
        headline = article.find('span', class_='WSJTheme--headlineText--He1ANr9C').text.strip()
        headlines.append(headline)
        
        # Extract published time
        published_time = article.find('p', class_='WSJTheme--timestamp--22sfkNDv').text.strip()
        published_times.append(published_time)

        # Extract article link
        link = article.find("a", href=True)["href"]
        article_links.append(link)

    # Create a Pandas DataFrame
    data = {
        'Topic': topics,
        'Headline': headlines,
        'Published Time': published_times,
        'URL': article_links
    }
    df = pd.DataFrame(data)

    return df