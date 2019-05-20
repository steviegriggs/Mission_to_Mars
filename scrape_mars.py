# Import Dependencies

from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
import numpy as np
from splinter import Browser


def scrape():

        #Start of Splinter

        # FOR MAC USERS ONLY
        # !which chromedriver

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)

        # NASA SCRAPE

        nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

        browser.visit(nasa_url)

        html = browser.html
        soup = bs(html, 'html.parser')

        news_title = browser.find_by_css('div[class="content_title"').text
        news_p = browser.find_by_css('div[class="article_teaser_body"').text



        # JPL SCRAPE

        jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        browser.visit(jpl_url)

        jpl_html = browser.html
        jpl_soup = bs(jpl_html, 'html.parser')

        browser.click_link_by_partial_text('FULL IMAGE')

        im_html = browser.html
        soup = bs(im_html, 'html.parser')

        img_obj = browser.find_by_css('img[class="fancybox-image"')
        featured_image_url = img_obj['src']


        # WEATHER SCRAPE

        weather_url = "https://twitter.com/marswxreport?lang=en"

        browser.visit(weather_url)

        weather_html = browser.html
        weather_soup = bs(weather_html, 'html.parser')

        for x in weather_soup.find_all('div', class_='js-tweet-text-container'):
                t = x.find('p').text
                if t[0:7] == 'InSight':
                        s = t.split('pic')
                        mars_weather = s[0].split('InSight ')[1]
                        break

        # FACTS SCRAPE

        facts_url = "https://space-facts.com/mars/"

        browser.visit(facts_url)
        facts_html = browser.html
        facts_soup = bs(facts_html, 'html.parser')

        facts_list = []

        table = facts_soup.find('table', id='tablepress-mars')
        table1 = table.find_all('tr')
        
        for x in table1:
                facts_list.append(x.text.strip())

        facts_1 = []
        facts_2 = []
        for x in facts_list:
                facts_1.append(x.split(':')[0])
                facts_2.append(x.split(':')[1])


        facts_df = pd.DataFrame(list(zip(facts_1, facts_2)))

        facts_html = facts_df.to_html(header = False, index = False)

        # HEMISPHERES SCRAPE

        hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

        browser.visit(hemisphere_url)

        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, 'html.parser')

        h = browser.find_by_css('a[class="itemLink product-item"')

        link_list = []
        title_list = []

        for x in range(len(h)):
                if x % 2 == 1:
                        y = h[x]
                        link_list.append(h[x]['href'])
                        z = y.find_by_tag('h3')
                        title_list.append(z.value)

        hrefs = []

        for link in link_list:
                browser.visit(link)
                href_test = []
                html = browser.html
                soup = bs(html, 'html.parser')
                ims = soup.find_all('a')
                for x in ims:
                        if x.text == 'Sample':
                                hrefs.append(x.get('href'))

        hemisphere_image_urls = []
        for x in zip(title_list, hrefs):
                hemisphere_image_urls.append({'title': x[0], 'img_url': x[1]})

        # END SPLINTER

        browser.quit()

        # Final Output
        
        return {
                "news_title": news_title,
                "news_paragraph": news_p,
                "jpl_img": featured_image_url,
                "weather": mars_weather,
                "mars_facts": facts_html,
                "hemispheres": hemisphere_image_urls
        }

# # TEST

# print(news_title)
# print(news_p)

# print('')
# print("----------")
# print('')

# print(featured_image_url)

# print('')
# print("----------")
# print('')

# print(mars_weather)

# print('')
# print("----------")
# print('')

# print(facts_html)

# print('')
# print("----------")
# print('')

# print(hemisphere_image_urls)