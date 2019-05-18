# -*- coding: utf-8 -*-

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from datetime import datetime

def scrape_news(browser):
    """Scrape one Mars news item form mars.nasa.gov (JPL).
    
    Returns output in dictionary form 
    {'success': success flag,
    'when_visited' : datetime object,
    'news_title': the news headling string, 
    'news_blob' : a short description of the news item (string)}
    if success==False, then 'news_title' will be an empty string, 
    and 'news_blob' will state 'no news found'
    """

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Record datetime for record-keeping
    when_visited = datetime.now()
    # Extraction protocol comes from manual site inspection
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        news_title = soup.find('div',class_='content_title').text
        news_blob = soup.find('div',class_='article_teaser_body').text
        success = True
    except AttributeError: 
        news_title = ''
        news_blob = 'no news found'
        success = False

    outputdict = dict(success=success, when_visited=when_visited, 
                      news_title=news_title, news_blob=news_blob)

    return outputdict
    
def scrape_featured_image(browser):
    """Scrape the Mars feature image from www.jpl.nasa.gov/spaceimages.
    
    Returns output in dictionary form 
    {'success': success flag,
    'when_visited' : datetime object,
    'featured_img_url': the url pointing to the hi-res jpeg version of the image}
    if success==False, then 'featured_img_url' returns a default url containing
    a static image
    https://www.nasa.gov/sites/default/files/thumbnails/image/pia22313.jpg
    """

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Record datetime for record-keeping
    when_visited = datetime.now()
    # Extraction protocol comes from manual site inspection
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        gallery = soup.find('section', class_='grid_gallery')\
                      .find('a',class_='fancybox')['data-fancybox-href']
        featured_img_url = 'https://jpl.nasa.gov' + gallery
        success = True
    except AttributeError: 
        featured_img_url = 'https://www.nasa.gov/sites/default/files/thumbnails/image/pia22313.jpg'
        success = False

    outputdict = dict(success=success, when_visited=when_visited, 
                      featured_img_url=featured_img_url)

    return outputdict

def scrape_weather_tweet(browser):
    """Scrape the Mars weather tweet from www.twitter.com/marswxreport.
    
    Returns output in dictionary form 
    {'success': success flag,
    'when_visited' : datetime object,
    'weather_tweet': the text of the latest weather tweet}
    if success==False, then 'weather_tweet' contains 'The latest weather
    tweet was not available.'
    """

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Record datetime for record-keeping
    when_visited = datetime.now()
    # Extraction protocol comes from manual site inspection
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        weather_tweet = soup.find('div', attrs={'data-screen-name':'MarsWxReport', 'class':'tweet'})\
                             .find('p', class_='js-tweet-text').text
        success = True
    except AttributeError: 
        weather_tweet = 'The latest weather tweet was not available.'
        success = False

    outputdict = dict(success=success, when_visited=when_visited, 
                      weather_tweet=weather_tweet)

    return outputdict

def scrape_fact_table(browser):
    """Scrape the Mars fact table from space-facts.com.
    
    Returns output in dictionary form 
    {'success': success flag,
    'when_visited' : datetime object,
    'fact_table': html string to display the fact table}
    if success==False, then 'fact_table' contains a default table that
    says 'No data available.'
    """

    url = 'http://space-facts.com/mars/'
    try:
        mars_df = pd.read_html(url)[0]
        fact_table = mars_df.to_html(header=False, index=False)
        success = True
    except (IndexError, requests.HTTPError):
        fact_table = """<table border="1" class="dataframe"><tbody> <tr>
        <td> No data available.</td> </tr></tbody></table>"""
        success = False
    # Record datetime for record-keeping
    when_visited = datetime.now()


    outputdict = dict(success=success, when_visited=when_visited, 
                      fact_table=fact_table)

    return outputdict

def scrape_hemispheres(browser):
    """Scrape the Mars hemisphere images from astrogeology.usgs.gov.
    
    Returns output in dictionary form 
    {'success': success flag,
    'when_visited' : datetime object,
    'image_info'': a list of four dictionaries comprising
                    {'title' : hemisphere name,
                    'img_url':the url for an image of the hemisphere}}
    if success==False, then 'image_info' contains four dictionaries with
    {'title': 'no name available','img_url':a place-holder 'sorry' image URL}
    """

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Record datetime for record-keeping
    when_visited = datetime.now()
    # Extraction protocol comes from manual site inspection
    html = browser.html
    soup = bs(html, 'html.parser')
    linklist = soup.find_all('a',class_='product-item')
    urllist = [item['href'] for item in linklist]
    # The links are in two places per item, so we only need every other one
    urllist2 = urllist[::2]
    # Build image list
    image_list = []
    if len(urllist2) > 0:
        for item in urllist2:
            newurl = 'https://astrogeology.usgs.gov' + item
            soupitem = bs(requests.get(newurl).text,'html.parser')
            hem_name = soupitem.find('h2').text[:-9]
            hem_imgurl = 'https://astrogeology.usgs.gov' + soupitem.find('img', class_ = 'wide-image')['src']
            image_list.append({'title':hem_name,'img_url':hem_imgurl})
        success = True
    else:
        for _ in range(4):
            image_list.append({'title':'no name available',
                            'img_url':'https://free-images.com/display/rose_background_excuse_me_1.html'})
        success = False
    
    outputdict = dict(success=success, when_visited=when_visited, 
                      image_list=image_list)

    return outputdict

def scrape():
    """Execute the scraping tasks (main function).
    
    The function will return a single dictionary in which
    the results from each scraping task will be stored as 
    a sub-dictionary"""

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    outputdict = {}
    # Insert all scraping steps here:
    outputdict['mars_news'] = scrape_news(browser)
    outputdict['mars_featured_image'] = scrape_featured_image(browser)
    outputdict['mars_weather'] = scrape_weather_tweet(browser)
    outputdict['mars_facts'] = scrape_fact_table(browser)
    outputdict['mars_hemispheres'] = scrape_hemispheres(browser)

    browser.quit()

    return outputdict


if __name__ == '__main__':
    scrape()