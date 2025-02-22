import time
import re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

URL = "https://www.reddit.com/r/wallstreetbets/top/?t=month"
SCROLL_PAUSE_TIME = 2
NUM_SCROLLS = 2
SLEEP_MS = 20

def parse_urls(url_list):
    result = []
    for str in url_list:
        match = re.search(r'href="([^"]+)"', str)
        if match:
            href_value = match.group(1)
            result.append("https://old.reddit.com" + href_value)
    result.pop(0)
    return result

# Extracts urls from main page
def scrape_urls():
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)
    driver.get(URL)

    scrape_list = []
    time.sleep(1)

    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(NUM_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        result = driver.find_elements(By.CSS_SELECTOR, "a[slot='full-post-link']")
        for element in result:
            scrape_list.append(element.get_attribute("outerHTML"))

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    return parse_urls(scrape_list)

# Takes list of urls and extracts post data
def scrape_posts(urls):
    posts = []
    for url in urls:
        posts.append(scrape_post(url))
        time.sleep(SLEEP_MS)
    return posts

# Takes post url and extracts data
def scrape_post(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='html.parser')

    # Check for request errors
    title_element = soup.find("title")
    if title_element.text == "Too Many Requests":
        return {'error': True}

    # Extract title
    post_title = ""
    post_title_element = soup.find("a", class_="title")
    if post_title_element:
        post_title = post_title_element.text
    
    # Extract post
    result = soup.find_all('p')
    sentences = []
    for i in range(18, len(result)):
        if result[i].text == "Post a comment!":
            break
        sentences.append(result[i].text)

    # Extract upvotes
    result = soup.find('div', class_="score")
    upvotes = result.find('span', class_='number').text

    # Extract comment count
    result = soup.find('div', class_="commentarea")
    comment_text = result.find('span', class_="title").text
    num_comments = comment_text.split()[1]

    return {
        'title': post_title,
        'body': sentences,
        'upvotes': upvotes,
        'num_comments': num_comments,
    }
    

# Tests for script
time.sleep(30)
print(scrape_post("https://old.reddit.com/r/wallstreetbets/comments/1igaaox/deepseek_reportedly_has_50000_nvidia_gpus_and/"))
time.sleep(30)
print(scrape_post("https://old.reddit.com/r/wallstreetbets/comments/1ip9ns8/flip_it/"))