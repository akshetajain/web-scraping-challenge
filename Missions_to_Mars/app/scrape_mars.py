# Import dependencies 
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Make a function
def scrape():
    scrape_dictionary = {}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select_one('ul.item_list li.slide')
    # Scrape Recent Headline
    results2 = results.find("div", class_="content_title")
    scrape_dictionary["Headline"] = results2.text
    # Scrape Description
    results3 = results.find("div", class_="article_teaser_body")
    scrape_dictionary["Description"] = results3.text

    # JPL MARS SPACE IMAGES
    # Start Scraping JPL Mars Space Images
    url2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    # Scrape image 
    image_jpl = soup2.find('a', class_ = 'fancybox-thumbs')['href']
    # Create image url link
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_jpl
    scrape_dictionary["Featured_Image"] = (featured_image_url)

    # MARS FACTS
    # Scrape Mars Facts
    mars_facts_df = pd.read_html('http://space-facts.com/mars/')[0]
    to_html_mars = mars_facts_df.to_html()
    scrape_dictionary["Mars_Facts"] = to_html_mars

    # MARS HEMISPHERES
    # Start Scraping Mars Hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    # Create a list of urls for images
    hemisphere_images = []
    hemisphere_links = browser.find_by_css("a.product-item h3")
    # For loop returns href
    for image in range(len(hemisphere_links)):
        dictionary = {}
        browser.find_by_css("a.product-item h3")[image].click()
        sample = browser.links.find_by_text('Sample').first
        dictionary['img_url'] = sample['href']
        dictionary['title'] = browser.find_by_css("h2.title").text
        hemisphere_images.append(dictionary)
        browser.back()
    scrape_dictionary["Hemisphere_Image_Links"] = hemisphere_images
    
    # RETURN DICTIONARY
    return scrape_dictionary
