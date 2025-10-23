import threading
import time
import re
import os
import pandas as pd
from queue import Queue, Empty
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import os

outputFile = "books_data_1.csv"
pages = 10
start_page = 1

pause = False 
reset = False

def set_pause(value):
    global pause
    pause = value

def set_reset(value):
    global reset
    reset = value


def createDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--headless=new")
    service = Service(r"") #Add the path here
    return webdriver.Chrome(service=service, options=options)

def initialize():
    if not os.path.exists(outputFile):
        columns = ["Title","Real Price","Discounted Price","Publisher","Pages","Weight","Dimensions","ISBN"]
        data_frame = pd.DataFrame(columns = columns)
        data_frame.to_csv(outputFile,index = False)
        print("CSV initialized")

def append(data):
    data_frame = pd.DataFrame([data])
    data_frame.to_csv(outputFile, mode="a",header=False,index=False)

def getUrls(driver,url):
    print(f"Getting URLs from: {url}")
    urls = []
    try:
        driver.get(url)
        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-dtl"))
        )
        
        for a in elements:
            try:
                href = a.find_element(By.TAG_NAME, "a").get_attribute("href")
                if href:
                    urls.append(href)
            except Exception:
                continue
                
        print(f"Found {len(urls)} book URLs.")
    except Exception as e:
        print(f"Error fetching URLs from {url}: {e}")
    return urls

def getBookData(driver,url):
    publisher = pages = weight = dimensions = isbn = "Not Provided"
    print(f'URL : {url}')
    driver.get(url)
    
    WebDriverWait(driver, 60).until_not(
        EC.presence_of_element_located((By.CLASS_NAME, "loading-screen-dots"))
    )
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    title_div = soup.find("div", class_="product-title")
    title = title_div.text.strip() if title_div else "Not Provided"

    disc_price_div = soup.find("span", class_=re.compile("sale-price"))
    disc_price = disc_price_div.text.strip().replace("Rs.", "").strip() if disc_price_div else "Not Provided"

    real_price_div = soup.find("del", class_=re.compile("real-price"))
    real_price = real_price_div.text.strip().replace("Rs.", "").strip() if real_price_div else "Not Provided"

    info = soup.find("div", class_="productinfo")
    if info:
        for div in info.find_all("div", recursive=False):
            spans = div.find_all("span")
            for span in spans:
                text = span.get_text(strip=True)
                sibling = span.find_next_sibling("span")
                value = sibling.get_text(strip=True) if sibling and sibling.get_text(strip=True) != "" else "Not Provided"
                
                if text == "Publisher:":
                    publisher = value
                elif text == "ISBN:":
                    isbn = value
                elif text == "Pages:":
                    pages = value
                elif text == "Shipping Weight:":
                    weight = value
                elif text == "Dimensions:":
                    dimensions = value

    return {
        "Title": title,
        "Real Price": real_price,
        "Discounted Price": disc_price,
        "Publisher": publisher,
        "Pages": pages,
        "Weight": weight,
        "Dimensions": dimensions,
        "ISBN": isbn,
    }

def worker(page_urls):
    driver = createDriver()
    
    for url in page_urls: 
        if reset:
            break
            
        while pause:
            print("Worker paused. Waiting for resume...")
            time.sleep(1)
            
        try:
            book = getBookData(driver, url) 
            
            if book["Title"] and book["Title"] != "Not Provided":
                print(f"Book : {book}")
                append(book)
            print(f"Scraped: {book['Title']}")
            
        except Exception as e:
            print(f"Error scraping data for {url}: {e}")
            continue
            
    driver.quit()

def start_scraping():
    """The main entry point for the scraping thread."""
    initialize()
    urls = []
    for i in range(start_page,pages):
        urls.append(f"https://www.readings.com.pk/category/level1/13/A/instock?page={i}") # Change the url
    
    driver = createDriver()
    for url in urls:
        if reset:
            break
            
        page_urls = getUrls(driver,url)
        
        worker(page_urls)
        
    driver.quit()
    print("Scraping Done")

if __name__ == '__main__':
    start_scraping()