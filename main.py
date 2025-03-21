import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if full_url.startswith(url):
                urls.add(full_url)
        return urls
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

def generate_sitemap(start_url, max_depth=2):
    sitemap = set()
    urls_to_visit = {start_url}
    visited_urls = set()

    for _ in range(max_depth):
        new_urls = set()
        for url in urls_to_visit:
            if url not in visited_urls:
                visited_urls.add(url)
                fetched_urls = fetch_urls(url)
                sitemap.update(fetched_urls)
                new_urls.update(fetched_urls)
        urls_to_visit = new_urls - visited_urls

    return sitemap

if __name__ == "__main__":
    start_url = "https://www.example.com" # Change this to the URL you want to generate a sitemap for your website
    sitemap = generate_sitemap(start_url)
    for url in sitemap:
        with open("sitemap.xml", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for url in sitemap:
                file.write(f"  <url>\n    <loc>{url}</loc>\n  </url>\n")
            file.write('</urlset>')