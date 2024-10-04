import requests
from bs4 import BeautifulSoup
import json
import sys
import subprocess
import os

# Define the path for the data folder
data_folder = os.path.join(os.path.dirname(__file__), 'data')

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

def web_scrape(query, output_file):
    # Ensure the output file has a .json extension and is saved in the data folder
    if not output_file.endswith(".json"):
        output_file = f"{output_file}.json"
    
    output_file_path = os.path.join(data_folder, output_file)

    # Format the query for the URL
    url = f"https://www.google.com/search?q={query}"

    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    # Send a GET request to Google Search
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        sys.exit(1)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the top 30 search result links
    results = []
    for index, item in enumerate(soup.select('h3')):
        parent = item.find_parent('a')
        if parent:
            link = parent['href']
            title = item.get_text()

            # Fetch the body content of the page
            body_content = fetch_body_content(link)
            
            # Add the original order and other details
            results.append({"original_order": index + 1, "title": title, "link": link, "content": body_content})

        if len(results) >= 30:  # Get top 30 results
            break

    if not results:
        print("No results found.")
        return

    # Save the results to the JSON file in the data folder
    with open(output_file_path, 'w') as json_file:
        json.dump(results[:30], json_file, indent=2)

    print(f"Data successfully scraped and saved to {output_file_path}")

def fetch_body_content(link):
    try:
        # Send a GET request to the individual link
        response = requests.get(link)

        if response.status_code != 200:
            print(f"Failed to retrieve content from {link}: {response.status_code}")
            return ""

        # Parse the HTML content of the page
        page_soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the body content
        body = page_soup.find('body')
        if body:
            return body.get_text(separator=' ', strip=True)
        else:
            return "No body content found."

    except Exception as e:
        print(f"Error fetching content from {link}: {str(e)}")
        return ""

def order_data(filename, keywords):
    # Define paths for ordering scripts
    ordering_python_path = os.path.join('implementations/webscraping/ordering.py')
    ordering_js_path = os.path.join('implementations/webscraping/ordering.js')

    # Check if the JSON file exists
    if not os.path.exists(filename):
        print("File not found. Please make sure the filename is correct.")
        return

    # Convert keywords to a comma-separated string for the subprocess call
    keyword_str = ','.join(keywords)

    # Attempt to call the Python ordering implementation
    try:
        result = subprocess.check_output(['python', ordering_python_path, filename, keyword_str])
        print("Python ordering implementation was successful.")
        return result.decode('utf-8')
    except subprocess.CalledProcessError:
        print("Python ordering implementation not found or failed. Trying JavaScript...")

    # If Python ordering failed, try JavaScript
    try:
        result = subprocess.check_output(['node', ordering_js_path, filename, keyword_str])
        print("JavaScript ordering implementation was successful.")
        return result.decode('utf-8')
    except subprocess.CalledProcessError:
        print("JavaScript ordering implementation not found or failed.")
        return None

if __name__ == "__main__":
    # Check command-line arguments for web scraping or ordering
    if len(sys.argv) < 3:
        print("Usage: python main.py <search_query> <output_file> OR python main.py <filename> <keyword1> <keyword2> ...")
        sys.exit(1)

    # Determine if we are scraping or ordering based on the number of arguments
    if len(sys.argv) == 3:
        # Perform web scraping
        search_query = sys.argv[1]
        output_filename = sys.argv[2]
        web_scrape(search_query, output_filename)
    else:
        # Perform ordering
        keywords = sys.argv[2:]  # Remaining arguments are keywords
        ordered_result = order_data(sys.argv[1], keywords)

        if ordered_result:
            print(f"Ordered data result:\n{ordered_result}")
        else:
            print("Ordering operation failed.")
