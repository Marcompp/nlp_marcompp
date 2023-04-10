import requests
from bs4 import BeautifulSoup
import sqlite3

# URL to crawl
url = "https://www.example.com"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the page content
page_content = str(soup)

# Connect to a SQLite database
conn = sqlite3.connect("crawl.db")

# Create a table to store the page content
conn.execute("CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY, url TEXT, content TEXT)")

# Insert the page content into the database
conn.execute("INSERT INTO pages (url, content) VALUES (?, ?)", (url, page_content))
conn.commit()

# Close the database connection
conn.close()