import sqlite3
from sqlite3 import IntegrityError
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import os
import time

def scrape_links(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Get the base URL for relative URL resolution
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Find all anchor tags (links) in the page
    links = soup.find_all("a")
    scraped_links = []

    for link in links:
        href = link.get("href")
        if href:
            # Resolve relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)
            scraped_links.append(absolute_url)

    return scraped_links


def scrape_and_store_page(url, output_dir):
    # Send a GET request to the webpage
    response = requests.get(url)
    html_content = response.text

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique output file name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"scraped_page_{timestamp}.html"
    html_file_path = os.path.join(output_dir, output_file)

    # Store the HTML content in a local file
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Page HTML scraped and stored as {html_file_path} successfully.")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find CSS links in the HTML
    css_links = soup.find_all("link", rel="stylesheet")

    # Download and store CSS files
    for css_link in css_links:
        css_url = urljoin(url, css_link["href"])
        css_response = requests.get(css_url)
        css_content = css_response.text

        css_file = os.path.basename(css_url)
        css_file_path = os.path.join(output_dir, css_file)
        with open(css_file_path, "w", encoding="utf-8") as file:
            file.write(css_content)

        print(f"CSS file {css_url} stored as {css_file_path} successfully.")


def scrape_and_get_text(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    main = soup.main

    if soup.find('main'): 
        text_elements = main.find_all(text=True)
    else: 
        text_elements = soup.find_all(text=True)
        
    # Join the text elements into a single string
    page_text = ' '.join(text_elements)

    return page_text


def store_page_text(url, output_dir):
    # Get the page text
    page_text = scrape_and_get_text(url)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the domain name from the URL
    domain = urlparse(url).netloc

    # Generate a unique output file name using the domain and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{domain}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    # Store the page text in a local file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(page_text)

    print(f"Page text stored as {filepath} successfully.")


def create_database():
    conn = sqlite3.connect("links.db")  # Connect to or create the database file
    c = conn.cursor()

    # Create a table to store the links
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  url TEXT)''')

    conn.commit()
    conn.close()

def store_links(links):
    conn = sqlite3.connect("links.db")
    c = conn.cursor()

    for link in links:
        try:
            c.execute("INSERT INTO links (url) VALUES (?)", (link,))
        except IntegrityError:
            # Link already exists in the database, skip insertion
            continue

    conn.commit()
    conn.close()


def query_links():
    # Connect to the SQLite database
    conn = sqlite3.connect("links.db")
    c = conn.cursor()

    # Execute an SQL query to select all URLs from the "links" table
    c.execute("SELECT url FROM links")
    rows = c.fetchall()

    # Close the database connection
    conn.close()

    # Extract the URLs from the result rows and store them in a list
    links = [row[0] for row in rows]
    return links


# # Starting point URL

# ## Create the links DB ###
# create_database()

# # Scrape all the links ###
# scraped_links = scrape_links(links_url)
# store_links(scraped_links)
# all_links = query_links()

# ## Print each link
# for link in all_links:
#    print(link)

# # Example usage
# output_dir = "files"
# scrape_and_store_page(url, output_dir)

# Example usage

output_dir = "files"
links=query_links()

counter = 0

for url in links:
    print("URL is ->", url)
    store_page_text(url, output_dir)
    counter += 1

    if counter == 100:
        break

    # Add a sleep timer of 1 second
    time.sleep(1)
