# Import necessary libraries
from bs4 import BeautifulSoup
import requests

# Define the URL of the site
url_to_scrape = 'http://example.com'

# Use requests to retrieve data from a given URL
response = requests.get(url_to_scrape)

# Parse the whole HTML page using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find a specific element using its tag name and (optional) its attributes
my_tag = soup.find('tag_name', attrs={'attribute_name': 'attribute_value'})

# Print the element
print(my_tag)
