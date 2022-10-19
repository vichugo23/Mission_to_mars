# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere_data": hemisphere_scrape(browser)
    }
     # Stop webdriver and return data
    browser.quit()
    return data

#creating a function for the first scrape. add the arguement inside the parantheses. in this case 'browser'. We are telling python that we'll be using the browser variable we defined outside our function. We need this to make our function to work bc our scraping code uses an automated 'browser'

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
        # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

# ## JPL Space Images Featured Image
#declare and define the function
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
       # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url



# ## Mars Facts
def mars_facts():
    #add try/except for error handling
    try:
        #use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    #Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# MARS HEMISPHERE SCRAPING

def hemisphere_scrape(browser) :
    # 1. Use browser to visit the URL 
    url =  'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with beautifulsoup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Get the links for each of the 4 hemispheres
    hemi_links = hemi_soup.find_all('h3')
    # hemi_links

    # loop through each hemisphere link
    for hemi in hemi_links:
        # Navigate and click the link of the hemisphere
        img_page = browser.find_by_text(hemi.text)
        img_page.click()
        html= browser.html
        img_soup = soup(html, 'html.parser')
        # Scrape the image link
        img_url = 'https://astrogeology.usgs.gov/' + str(img_soup.find('img', class_='wide-image')['src'])
        # Scrape the title
        title = img_soup.find('h2', class_='title').text
        # Define and append to the dictionary
        hemisphere = {'img_url': img_url,'title': title}
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        # print(hemisphere_image_urls)
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())






