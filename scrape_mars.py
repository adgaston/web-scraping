from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create mars_data Dictionary
    mars_data = {}
    #-----------------------------------

    # Visit NASA Mars News Site
    mars_news_url = 'https://mars.nasa.gov/news/'
    news_results = browser.visit(mars_news_url)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    news_results = news_soup.find_all('div', class_='slide')
    news_dict = []

    # Grab News Titles & Details
    for result in news_results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.a.div.text

        # Save to a Dictionary 
        news_dictionary = {
            'news_title': news_title, 
            'news_detail': news_p
            }
        news_dict.append(news_dictionary)  
    
    # Add to mars_data
    mars_data["news_data"] = news_dict
    #-----------------------------------

    # Visit JPL Featured Space Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Design an XPATH selector to direct Splinter to click the FULL IMAGE button
    xpath = '/html/body/div[1]/div/div[3]/section[1]/div/div/article/div[1]/footer/a'

    # Click FULL IMAGE button to get full-size image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    time.sleep(3)

    # Grab the image link
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    img_url = jpl_soup.find('img', class_='fancybox-image')['src']

    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + img_url
   
    # Add to mars_data
    mars_data["featured_image_url"] = featured_image_url
    #-----------------------------------

    # Visit Mars Weather Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    html = browser.html
    twitter_soup = BeautifulSoup(html, 'html.parser')

    # Retrieve Recent Tweet
    mars_weather = twitter_soup.find('div', class_='js-tweet-text-container').text.strip()
    
    # Add to mars_data
    mars_data["mars_weather_tweet"] = mars_weather
    #-----------------------------------

    # Visit Mars Facts
    url = 'https://space-facts.com/mars/'

    # Read Table
    tables = pd.read_html(url)

    # Save Table as DataFrame
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)

    # Save DataFrama as HTML element
    facts_df.to_html('table.html')
    #-----------------------------------

    # Visit Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    # Design an XPATH selector to direct Splinter to click the Hemisphere Link
    xpath1 = '/html/body/div/div[1]/div/section/div/div[2]/div['
    xpath2 = ']/div/a'

    hemisphere_image_urls = []

    for x in range(1,5):
        # Clicking the Hemisphere Links to get to next page
        xpath = xpath1 + str(x) + xpath2
        results = browser.find_by_xpath(xpath)
        img = results[0]
        img.click()
    
        # Soup
        html = browser.html
        hemi_soup = BeautifulSoup(html, 'html.parser')
    
        # Grab the link
        iresults = hemi_soup.find_all('div', class_='downloads')
        for result in iresults:
            img_url = result.find('a', href=True)['href']
    
        # Grab the link
        tresults = hemi_soup.find_all('div', class_='content')
        for result in tresults:
            title = result.find('h2', class_='title').text
            title = title.replace(' Enhanced', '')
    
        # Save to a Dictionary and post to DB
        hemisphere_dict = {
            'title': title, 
            'img_url': img_url
            }
        hemisphere_image_urls.append(hemisphere_dict)   
    
        # Go back to Home Page in browser
        browser.back()
    
    # Add to mars_data
    mars_data["hemispheres_info"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data