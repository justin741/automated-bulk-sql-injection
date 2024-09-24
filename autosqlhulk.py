import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def google_search(query, max_pages=10):
    urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    for page in range(max_pages):
        start = page * 10
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"
        
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links_found = False
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'url?q=' in href:
                    # Extract the actual URL
                    url = href.split('url?q=')[1].split('&')[0]
                    urls.append(url)
                    links_found = True
            
            if not links_found:
                print("No more links found.")
                break
        else:
            print(f"Failed to retrieve page {page + 1}")
            break
        
        # Be polite and don't overwhelm the server
        time.sleep(2)  # Delay to avoid being blocked
    
    return list(set(urls))  # Return unique URLs

def save_urls_to_file(urls, filename='urls.txt'):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url + '\n')

if __name__ == "__main__":
    query = "your dork query here"  # Replace with your actual query
    result_urls = google_search(query, max_pages=10)
    save_urls_to_file(result_urls, 'urls.txt')
    print(f"Saved {len(result_urls)} URLs to urls.txt.")
