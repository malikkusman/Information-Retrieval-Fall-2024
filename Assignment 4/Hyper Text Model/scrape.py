import requests
from bs4 import BeautifulSoup
import json

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Pakistan"
base_url = "https://en.wikipedia.org"  # Base URL for relative links

# Make a request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract headings and paragraphs with hyperlinks and references
content = {}
current_section = None

# Function to get formatted text with hyperlinks and citations
def format_content(element):
    if element.name == 'a':
        href = element.get('href')
        # Convert relative URLs to absolute
        if href and href.startswith('/'):
            href = base_url + href
        link_text = element.text
        return f'<a href="{href}" target="_blank">{link_text}</a>'
    elif element.name == 'sup':
        return f'<sup>{element.text}</sup>'
    return element.text

# Loop through all elements and capture content under each heading
for element in soup.find_all(['h2', 'h3', 'p']):
    if element.name in ['h2', 'h3']:
        # This is a heading, so we start a new section
        current_section = element.text.strip()
        content[current_section] = []
    elif element.name == 'p' and current_section:
        # This is a paragraph under the current section
        paragraph = ''.join(format_content(child) for child in element.children)
        content[current_section].append(paragraph)

# Filter out sections that have empty lists
content = {section: paragraphs for section, paragraphs in content.items() if paragraphs}

# Save the structured content to a JSON file
with open('pakistan_content.json', 'w') as f:
    json.dump(content, f, indent=4)

print("Content scraped and saved to 'pakistan_content.json'")
