import requests
from bs4 import BeautifulSoup
import json
import sys
import subprocess
import os
import random

# Define the paths for the data and result folders
data_folder = os.path.join(os.path.dirname(__file__), 'data')
result_folder = os.path.join(os.path.dirname(__file__), 'results')

# Create the result folder if it doesn't exist
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

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
    print(response)
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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/"
        }

        # Optionally, add proxy handling
        # proxies = {
        #     'http': 'http://your-proxy-server:port',
        #     'https': 'https://your-proxy-server:port'
        # }

        # Send the GET request
        response = requests.get(link, headers=headers)

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
    # Generate a random 3-digit number for versioning
    version_number = random.randint(100, 999)
    
    # Define paths for ordering scripts
    ordering_python_path = os.path.join(os.path.dirname(__file__), 'ordering.py')
    ordering_js_path = os.path.join(os.path.dirname(__file__), 'ordering.js')

    # Full path to the JSON file in the data folder
    json_file_path = os.path.join(data_folder, f"{filename}.json")

    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print(f"File '{filename}.json' not found in the data folder.")
        return

    # Define output file path in the result folder with version number
    output_file_name = f"{filename}_version{version_number}.json"
    output_file_path = os.path.join(result_folder, output_file_name)
    
    # Convert keywords to a comma-separated string for the subprocess call
    keyword_str = ','.join(keywords)

    # Attempt to call the Python ordering implementation
    try:
        result = subprocess.check_output(['python', ordering_python_path, json_file_path, keyword_str, output_file_path])
        print(f"Python ordering implementation was successful. Ordered file saved as {output_file_name}")
        return output_file_name
    except subprocess.CalledProcessError:
        print("Python ordering implementation failed. Trying JavaScript...")

    # If Python ordering failed, try JavaScript
    try:
        result = subprocess.check_output(['node', ordering_js_path, json_file_path, keyword_str, output_file_path])
        print(f"JavaScript ordering implementation was successful. Ordered file saved as {output_file_name}")
        return output_file_name
    except subprocess.CalledProcessError:
        print("JavaScript ordering implementation failed.")
        return None

if __name__ == "__main__":
    # Check command-line arguments for web scraping or ordering
    if len(sys.argv) < 2:
        print("Usage: python main.py <'webscrape'/'order'> <other arguments>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "webscrape" and len(sys.argv) == 4:
        # Perform web scraping
        search_query = sys.argv[2]
        output_filename = sys.argv[3]
        web_scrape(search_query, output_filename)

    elif command == "order" and len(sys.argv) >= 4:
        # Perform ordering
        filename = sys.argv[2]
        keywords = sys.argv[3:]  # Remaining arguments are keywords
        ordered_result = order_data(filename, keywords)

        if ordered_result:
            print(f"Ordered data result:\n{ordered_result}")
        else:
            print("Ordering operation failed.")
    else:
        print("Invalid usage. Correct format:\n"
              "For web scraping: python main.py webscrape <search_query> <output_file>\n"
              "For ordering: python main.py order <filename> <keyword1> <keyword2> ...")
