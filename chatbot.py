import sys
import json
import re
import requests
from bs4 import BeautifulSoup

def scrape_crescent_website():
    # URL to scrape
    url = "https://crescent.education"

    try:
        # Perform the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all links from the page
        links = {}
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True)
            href = link["href"]
            if href.startswith("http"):  # Absolute URL
                links[text] = href
            else:  # Handle relative URLs
                absolute_url = requests.compat.urljoin(url, href)
                links[text] = absolute_url

        return links

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}

def extract_keywords(user_input):
    # Common words to ignore in user input
    ignore_words = {"i", "need", "details", "information", "about", "please", "give", "me"}

    # Clean the user input and split it into words
    words = re.sub(r'[^a-zA-Z0-9\s]', '', user_input.lower()).split()

    # Remove ignored words
    filtered_words = [word for word in words if word not in ignore_words]

    # Join filtered words to form the core phrase
    return " ".join(filtered_words)

def get_response(user_input):
    # Simple responses for basic greetings
    simple_responses = {
        "hi": "Hello!",
        "hello": "Hi there!",
        "bye": "Goodbye!",
    }

    # Clean the user input
    cleaned_input = extract_keywords(user_input)

    # Check for simple responses
    if cleaned_input in simple_responses:
        return simple_responses[cleaned_input]

    # Scrape all links
    all_links = scrape_crescent_website()

    # Find the best matching link using substring matching
    for text in all_links:
        if cleaned_input in text.lower():  # Check if the cleaned input matches any link text
            link = all_links[text]
            return f"<a href='{link}' target='_blank'>{text}</a>"

    # Default fallback response if no match is found
    return "Sorry, I couldn't find any matching links."

if __name__ == "__main__":
    # Read user input from the command line
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = ""

    # Get the chatbot's response
    response = get_response(user_input)

    # Output the response in JSON format
    print(json.dumps({"response": response}))
