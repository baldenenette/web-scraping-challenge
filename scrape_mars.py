#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time as time
from pprint import pprint


# # Mac Users

# In[2]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# get_ipython().system('which chromedriver')
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)
sleep_delay = 5

def click_link(button_text):
        browser.click_link_by_partial_text(button_text)
        time.sleep(sleep_delay)

        html = browser.html
        ret_soup = BeautifulSoup(html, "html.parser")
        return ret_soup

    # Function cleans up text by removing "\", removing " Enhanced" and replacing " with '
def clean_text(text_to_clean):
    cleaned_text = text_to_clean.replace("\'", "'")
    cleaned_text = cleaned_text.replace('"', "'")
    cleaned_text = cleaned_text.replace(' Enhanced', "")
    cleaned_text = cleaned_text.replace("\n", "")

    return cleaned_text

# In[3]:
def scrape():   

    # # NASA Mars News
    #

    # In[4]:

    # Visit NASA URL to scrape the page
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(sleep_delay)
    # In[5]:

    

    # In[6]:

    html = browser.html

    # In[7]:

    # Visit the NASA Mars News Site
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # In[8]:

    # Collect the latest News Title and Paragraph Text

    news_title = clean_text(soup.find_all(
        "div", class_="content_title")[1].find("a").text)
    print(news_title)

    news_p = clean_text(soup.find_all("div", class_="image_and_description_container")[
                        0].find("div", class_="article_teaser_body").text)
    pprint(news_p)

    # In[9]:

    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)

    # # JPL Mars Space Images - Featured Image

    # In[10]:

    # define the url and visit it with browser

    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(mars_image_url)

    # In[11]:

    # click on the Full Image button. I couldn't get it to work with partial text, so used the id.

    browser.click_link_by_id('full_image')

    # In[12]:

    browser.click_link_by_partial_text('more info')

    # In[13]:

    # create the soup item

    image_html = browser.html
    mars_image_soup = BeautifulSoup(image_html, 'html.parser')

    # the large image is within the figue element with class = lede
    image = mars_image_soup.body.find("figure", class_="lede")

    # the url is within the a element, so search for a element and then extract the url
    link = image.find('a')
    href = link['href']

    # define the beginning of the url as the returned href doesn't included it
    base_url = 'https://www.jpl.nasa.gov'

    # create the full url
    featured_image_url = base_url + href

    featured_image_url

    # # Mars Weather

    # In[13]:

    # Visit Twitter url for latest Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    html = browser.html
    response = requests.get(tweet_url)

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract latest tweet
    tweet_container = soup.find_all('p', class_="js-tweet-text")

    print(tweet_container)

    # In[15]:

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container:
        mars_weather = tweet.text
        if 'sol' and 'pressure' in mars_weather:
            mars_weather = mars_weather.split('pic')[0]
            print(mars_weather)

            break
        else:
            pass

    # # Mars Facts
    # Visit the Mars Facts webpage.
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    # In[18]:

    mars_facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(mars_facts_url)

    df1 = tables[0]
    
    df1.columns = ["Description", "Value"]
    df1.set_index("Description", inplace=True)

    df1=df1.to_html()

    # # Mars Hemispheres

    # In[21]:

    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_="result-list")
    hemispheres = results.find_all("div", class_="item")

    # loop through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Print image title and url
    print(hemisphere_image_urls)
    return({
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_table": df1,
        "hemisphere_image_urls": hemisphere_image_urls

    })
