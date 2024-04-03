import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Function to scrape all headlines on WSJ on a given day
def scrape_wsj_date(date):
    # Base URL
    base_url = f'https://www.wsj.com/news/archive/{str(date.year)}/{str(date.month).zfill(2)}/{str(date.day).zfill(2)}?page='

    # Initialize lists to store data
    all_articles = []

    # Create page counter
    page_num = 1

    # Define header
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # Loop through each page
    while True:
        # URL of the webpage to scrape
        url = base_url + str(page_num)

        # Open the webpage
        response = requests.get(url, headers=headers)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all articles on the page
        articles = soup.find_all('article')

        # Exit loop if no more articles on page
        if not articles: 
            break
        
        all_articles.extend(articles)
        
        # Increment page
        page_num += 1

    return all_articles

# Function to scrape all articles on WSJ on a given date range
def scrape_wsj_date_range(start_date, end_date):
    # Initialize an empty list to store all articles
    all_articles = []

    # Iterate over each date in the specified range
    for current_date in pd.date_range(start_date, end_date):
        # Scrape articles for the current date
        articles_for_date = scrape_wsj_date(current_date)
        
        # Extend the list of all_articles with the articles for the current date
        all_articles.extend(articles_for_date)
    
    return all_articles

# Function to scrape all articles on WSJ on a given date range and return dataframe output
def scrape_wsj(start_date, end_date):
    # Scrape articles in given date range
    articles = scrape_wsj_date_range(start_date, end_date)

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