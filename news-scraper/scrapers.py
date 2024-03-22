from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape all headlines on WSJ on a given day
# ONLY SCRAPES PAGE 1 FOR NOW
def scrape_wsj(year, month, date):
    # Start a WebDriver (you need to have chromedriver installed in your system and its path added to the environment variables)
    driver = webdriver.Chrome()

    # URL of the webpage to scrape
    url = f'https://www.wsj.com/news/archive/{year}/{month}/{date}'

    # Open the webpage
    driver.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the WebDriver
    driver.quit()
  
    # Initialize lists to store data
    topics = []
    headlines = []
    published_times = []

    # Find all articles on the page
    articles = soup.find_all('article')

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

    # Create a Pandas DataFrame
    data = {
        'Topic': topics,
        'Headline': headlines,
        'Published Time': published_times
    }

    df = pd.DataFrame(data)

    return df