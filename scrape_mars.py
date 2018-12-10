import pandas as pd
import requests
import splinter
from bs4 import BeautifulSoup as bs

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = splinter.Browser('chrome', **executable_path, headless=False)


def make_soup(url):
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    return soup


def scrape():
    # GET news
    news_url = 'https://mars.nasa.gov/news/'
    news_soup = make_soup(news_url)

    news_title = news_soup.body.find(class_='content_title').text
    news_p = news_soup.body.find(class_='article_teaser_body').text

    # GET imgs
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.click_link_by_id('full_image')
    img_soup = make_soup(img_url)

    img_el = img_soup.body.find('img', class_='fancybox-image')
    featured_img_url = f"{img_url}{img_el.attrs['src']}"

    # GET tweet
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_soup = make_soup(twitter_url)

    mars_weather = twitter_soup.body.find(class_='js-tweet-text').text

    # GET fact table
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)

    facts_df = pd.read_html(facts_url)[0].rename(
        columns={0: "key", 1: "value"})
    facts_table_html = facts_df.to_html()

    # GET hemisphere img urls
    hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hems_soup = make_soup(hems_url)

    hem_urls = []
    hem_titles = []
    hemisphere_image_urls = []

    for i in hems_soup.body.findAll(class_='product-item'):
        j = i.text.split(' ')[:-1]
        if(len(j) > 0):
            k = ' '.join(list(filter(lambda a: a != '', j)))
            hem_titles.append(k)

    for i in hem_titles:
        browser.click_link_by_partial_text(i)
        soup = bs(browser.html, 'html.parser')
        hem_urls.append(soup.find(class_='downloads').a.attrs['href'])
        browser.visit(hems_url)

    for i in range(4):
        hemisphere_image_urls.append(
            {'title': hem_titles[i], 'img_url': hem_urls[i]})

    browser.quit()

    return news_title, news_p, featured_img_url, mars_weather, facts_table_html, hemisphere_image_urls
