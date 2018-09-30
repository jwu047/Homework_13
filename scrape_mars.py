
# coding: utf-8
# Dependencies
import os
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver

# Connect to chromedriver
def init_browser():
# Windows Users (ex: 13.2.7)
    executable_path = {'executable_path': 'chromedriver.exe'}
    # Chrome59 headless browser, https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    browser = Browser('chrome', **executable_path, headless=True)
    #nasa_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #browser.visit(nasa_url)
    return browser


def scrape():

    # We need something to put the data in
    scraped_mars_data = {}

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    #print(soup.prettify())

    # Get the latest news
    results = soup.find('div', class_ = 'features')
    #for result in results:
        #print(result)

    #Assign the text to variables that you can reference later
    news_title = results.find('div', class_ = 'content_title').text
    #print(news_title)
    news_p = results.find('div', class_ = 'rollover_description').text
    #print(news_p)

    # !! Store data into the newly created dictionary
    scraped_mars_data['news_title'] = news_title
    scraped_mars_data['news_p'] = news_p

    # Visit the Mars Weather twitter account "https://twitter.com/marswxreport?lang=en", scrape the latest Mars weather tweet
    # Save the tweet text for the weather report as a variable called mars_weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_response = requests.get(twitter_url)
    twitter_bs = bs(twitter_response.text, 'lxml')
    
    twitter_results = twitter_bs.find('div', class_ = 'js-tweet-text-container')
    mars_weather = twitter_results.find('p', class_ = 'js-tweet-text').text
    #mars_weather

    scraped_mars_data['mars_weather'] = mars_weather

    # Mars Facts
    # Visit Mars Facts, https://space-facts.com/mars/, use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to an HTML table string.
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    #table

    df = table[0]
    df.columns = ['Measurement', 'Value']
    #df.head()
    df.set_index('Measurement', inplace = True)
    #df.head()

    # HTML table string
    mars_html_table = df.to_html()
    mars_html_table.replace("\n", "")
    df.to_html('mars_html_table.html')

    #Store
    scraped_mars_data['mars_facts'] = mars_html_table

    #Images from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    #Use Splinger to find the image url for the current Featured Mars Image 
    # chromedriver function for splinter
    browser = init_browser()

    # Last featured image of mars
    nasa_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_url)

    nasa_html = browser.html
    #nasa_html
    nasa_bs = bs(nasa_html, "lxml")
    #nasa_bs


    # inspect element to get to featured, use beautiful soup's find() method (ex:13.2.8)
    featured = nasa_bs.find('div', class_ = 'default floating_text_area ms-layer')
    featured_image = featured.find('footer')
    # look through the anchors, a
    featured_url = 'https://www.jpl.nasa.gov' + featured_image.find('a')['data-fancybox-href']
    #print(str(featured_url))


    #Store
    scraped_mars_data['featured_image_url'] = featuerd_url
    # # Mars Hemispheres


    # USGS Astrogeology site, https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    # Use python dictionary to store the data using the keys img_url and title
    # Append the dictionary with the image url string and the hemisphere title to a list
    # This will contain one ictionary for each hemisphere
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_bs = bs(hemisphere_html, 'lxml')
    base_url = "https://astrogeology.usgs.gov"
    # inspect div.item
    images = hemisphere_bs.find_all('div', class_ = 'item')

    # a list of dictionaries
    hemisphere_image_urls = []





    # loops through list of images, finds larger resolution image url for each hemisphere
    for image in images:
        
        # provided format
        hemisphere_dictionary = {}
        
        # ex:(13.2.8), under h3, looking for anchors
        href = image.find('a', class_ = 'itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)

        # link html
        html2 = browser.html
        bs2 = bs(html2, 'lxml')
        
        # div.content container, h2.title for title, 
        image_title = bs2.find('div', class_ = 'content').find('h2', class_ = 'title').text
        hemisphere_dictionary["title"] = image_title
        
        # inspect under download portion with sample and original
        image_url = bs2.find('div', class_ = 'downloads').find('a')['href']
        hemisphere_dictionary["img_url"] = image_url
        
        # add the created dictionary into the initial empty list
        hemisphere_image_urls.append(hemisphere_dictionary)

    # check
    #hemisphere_image_urls
    
    #Store
    scraped_mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return scraped_mars_data