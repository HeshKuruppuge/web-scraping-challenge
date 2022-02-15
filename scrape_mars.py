from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


    #################################################
    # Main Web Scraping 
    #################################################
def scrape_all():
    
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    
    # Store all scraped data in a dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data 
    
       
    
    ##############################################################
    # Title and the News
    ###############################################################
    
def mars_news(browser):
    
    # Visit URL
    url = "https://redplanetscience.com/"
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
        
    # Scrape page into Soup
    html = browser.html
    news_soup = soup(html, 'html.parser')  
    
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
    
       #Find the latest title
        news_title=slide_elem.find("div", class_='content_title').get_text()
    
       # Find the related paragraphs on above title
        news_para = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    
    except AttributeError:
        return None, None
    
    return news_title, news_para
    
     ##############################################################
    # JPL Mars Space Images - Featured Image
    ###############################################################
def featured_image(browser):
    
    url="https://spaceimages-mars.com/"
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
    
    
     ##############################################################
    # Mars Fact
    ###############################################################
def mars_fact():
    
    try:
        # Read and get the html data to a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com/')[0] 
        
    except BaseException:
        return None

    #name the columns and set index
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    #convert the data to a HTML table 
    return df.to_html(classes="table table-striped")
    
     ##############################################################
    # Mars Hemispheres
    ###############################################################
def hemispheres(browser): 
    
    url= "https://marshemispheres.com/"
    browser.visit(url)
    
    #define list to hold images 
    hemisphere_image_urls =[]
    
    #find the image links
    #links=browser.find_by_css("a.product-item img")
    
    # Iterate through the image link collection
    for item in range(4):
        #hemisphere = {}
    
        # We have to find the elements on each loop 
        browser.find_by_css('a.product-item img')[item].click()
    
        # Extract the href link from anchor tag 
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
        # Get the title
        hemisphere['title'] = browser.find_by_css('h2.title').text
    
        # Append to list
        hemisphere_image_urls.append(hemisphere)
    
        # navigate backwards
        browser.back()
        
    return hemisphere_image_urls

      
     ##############################################################
    #def scrape_hemisphere(html_text):
    ###############################################################
   
def scrape_hemisphere(html_text):
    # parse html text
    hemi_soup = soup(html_text, "html.parser")

    # adding try/except 
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":

    
    print(scrape_all())

    

    