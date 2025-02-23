import time
import re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import csv

URL = "https://www.reddit.com/r/wallstreetbets/top/?t=month"
SCROLL_PAUSE_TIME = 5
NUM_SCROLLS = 2
SLEEP_MS = 0

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
        #time.sleep(SLEEP_MS)
    return posts

# Takes post url and extracts data
def scrape_post(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = requests.get(url, headers=headers)
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
    body = ""
    for i in range(18, len(result)):
        if result[i].text == "Post a comment!":
            break
        body += result[i].text

    # Extract upvotes
    result = soup.find('div', class_="score")
    upvotes = result.find('span', class_='number').text

    # Extract comment count
    result = soup.find('div', class_="commentarea")
    comment = result.find('a', class_="title-button")
    num_comments = 0
    if not comment:
        comment = result.find('span', class_="title")
        num_comments = comment.text.split()[1]
    else:
        num_comments = comment.text.split()[-1]

    return {
        'title': post_title,
        'body': body,
        'upvotes': int(upvotes.replace(",", "")),
        'num_comments': int(num_comments),
    }
    
urls = scrape_urls()
posts = scrape_posts(urls)

with open("output.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=posts[0].keys())
    writer.writeheader()
    writer.writerows(posts)