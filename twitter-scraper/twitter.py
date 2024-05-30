from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service  
import time  
import re  

# Initialize the Selenium WebDriver
def initialize_driver():
    service = Service(r'C:\Users\eslam elgendy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Specify path chromedriver
    driver = webdriver.Chrome(service=service)  # Initialize Chrome WebDriver with specified service
    return driver  

# Scroll the page down by 2000 pixel by n times 
def scroll(driver, n_scroll):
    for i in range(n_scroll):  # Loop to scroll the page n times
        driver.execute_script("window.scrollBy(0, 2000)")  # Execute JavaScript to scroll down the page
        time.sleep(1)  # Wait for 1 second to allow content to load

# Get tweets using Selenium
def get_tweets(driver, account):
    url = f"https://twitter.com/{account}"  # Construct the URL for the user's Twitter page
    driver.get(url)  # Use the WebDriver to open the URL

    time.sleep(5)  # Wait for the page to load

    scroll(driver, 8)  # Scroll the page to load more tweets

    tweets = []
    # Xpath for the tweets
    xpath = '//div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[2]'

    # Locate all tweets on the page
    tweet_elements = driver.find_elements(By.XPATH, xpath)
    for tweet in tweet_elements:  
         tweets.append(tweet.text)  # Extract the tweet text and append it into a list
    return tweets

# Count mentions of the tricker
def count_mentioned(tweets, ticker):
    pattern = re.compile(fr'[\#\$]?{ticker}\b', re.IGNORECASE)  # Regex pattern to match the ticker, case insensitive
    count = 0 
    for tweet in tweets:  # Iterate over each tweet
        if pattern.search(tweet):  # Search for the ticker pattern in the tweet
            count += 1  # Increment the counter if the pattern is found
    return count  


def main(accounts, ticker, interval):
    driver = initialize_driver()  # Initialize the Selenium WebDriver
    while True: 
        total_mention = 0  # Initialize the total mentions counter

        for account in accounts:  # Iterate over each Twitter account
            tweets = get_tweets(driver, account)  # Get tweets for the current account
            mention = count_mentioned(tweets, ticker)  # Count the mentions of the ticker in the tweets
            total_mention += mention  

            print(f"Account: https://twitter.com/{account} has {mention} mentions")  

        print(f"Total mentions of {ticker}: {total_mention} times in the last {interval / 60} minutes")  

        time.sleep(interval)  # Wait for the specified interval before repeating


if __name__ == "__main__":
    accounts = [
        "Mr_Derivatives", 
        "warrior_0719", 
        "ChartingProdigy", 
        "allstarcharts", 
        "yuriymatso", 
        "TriggerTrades", 
        "AdamMancini4", 
        "CordovaTrades", 
        "Barchart",
        "RoyLMattox"
    ]
    ticker = "SPX"  # Set the word to look for
    interval = 60 * 5  # Time interval in seconds
    main(accounts, ticker, interval)  
