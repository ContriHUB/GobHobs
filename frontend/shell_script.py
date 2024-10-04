import cmd
import requests
import json
import os

class WebScraperSubCLI(cmd.Cmd):
    intro = "Welcome to the Goblin Web Scraping CLI. Type help or ? to list commands.\n"
    prompt = "(goblin-webscrape) "

    
    def do_websearch(self, arg):
        """Perform a web search and get results."""
        query = input("Enter search query: ")
        output_file = input("Enter output JSON filename: ")

        response = requests.post('http://localhost:5000/webscrape', json={"query": query, "output_file": output_file})
        
        # Print the full response to see what's returned
        print("Full response from web scraping API:", response.json())

        # Check if 'result' exists in the response
        if 'result' in response.json():
            print("Web scraping result:\n", response.json()['result'])
        else:
            print("Error:", response.json().get('error', 'Unknown error occurred.'))




    def do_order(self, arg):
        """Order the web scraped data."""
        filename = input("Enter the JSON file name (with path): ")
        num_keywords = int(input("Enter number of keywords for ordering: "))
        keywords = []

        for _ in range(num_keywords):
            keyword = input("Enter a keyword: ")
            keywords.append(keyword)

        # Make a request to the backend to order the data
        response = requests.post('http://localhost:5000/order', json={"filename": filename, "keywords": keywords})
        print("Ordering result:\n", response.json()['result'])




    def do_viewdata(self, arg):
        """View the scraped JSON data."""
        filename = input("Enter the filename of the JSON data to view (without extension): ")
        filepath = os.path.join(os.path.dirname(__file__), '../implementations/webscraping/data', f"{filename}.json")

        if os.path.exists(filepath):
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                print(json.dumps(data, indent=2))  # Pretty-print JSON
        else:
            print(f"{filename}.json not found.")

    def do_exit(self, arg):
        """Exit the Goblin Web Scraping CLI."""
        print("Exiting Goblin Web Scraping CLI.")
        return True

class PhoneRecordsSubCLI(cmd.Cmd):
    intro = 'PhoneRecords CLI. Type help or ? to list commands.\n'
    prompt = '(phonerecords) '

    def do_createjson(self, arg):
        'Create a JSON file from a CSV file in the samplecsv folder.\nUsage: createjson <csv_filename>'
        csv_filename = input("Enter the CSV filename (without .csv extension): ")

        # Call the backend API to convert the CSV to JSON
        try:
            response = requests.post('http://127.0.0.1:5000/createjson', json={
                'csv_filename': csv_filename
            })

            if response.status_code == 200:
                print(response.json()['message'])
            else:
                print(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Error during request: {str(e)}")


    def do_search(self, arg):
        'Search for a record in the JSON file.\nUsage: search <json_filename> <field> <search_term>'
        filename = input("Enter the filename of the JSON data to search (without extension): ")
        field_index = input("Enter the field index (1 for name, 2 for address, etc.): ")
        search_term = input("Enter the keyword to search: ")

        # Call the backend API to search the JSON file
        try:
            response = requests.post('http://127.0.0.1:5000/search', json={
                'filename': filename,
                'field': field_index,
                'search_term': search_term
            })

            if response.status_code == 200:
                result = response.json()['result']
                print(f"Search result:\n{result}")
            else:
                print(f"Error: {response.json().get('error', 'Unknown error occurred')}")
        except Exception as e:
            print(f"Error during request: {str(e)}")

    def do_back(self, arg):
        'Return to the main GoblinExtractor CLI.'
        return True


class PDFExtractorSubCLI(cmd.Cmd):
    intro = 'Welcome to the PDF Extractor CLI. Type help or ? to list commands.\n'
    prompt = '(pdfextractor) '

    def do_extract(self, arg):
        'Extract data from a PDF and convert it to JSON.\nUsage: extract <pdf_filename_without_extension>'
        pdf_filename = input("Enter the PDF filename (without .pdf extension): ")

        # Call the backend API to extract data from the PDF
        response = requests.post('http://127.0.0.1:5000/extractpdf', json={'filename': pdf_filename})

        if response.status_code == 200:
            print(response.json()['message'])
        else:
            print(f"Error: {response.json()['error']}")

    def do_view(self, arg):
        'View the extracted JSON data.\nUsage: view <json_filename_without_extension>'
        json_filename = input("Enter the JSON filename (without .json extension): ")

        # Call the backend API to view the JSON data
        response = requests.post('http://127.0.0.1:5000/viewjson', json={'filename': json_filename})

        if response.status_code == 200:
            print(response.json()['data'])
        else:
            print(f"Error: {response.json()['error']}")

    def do_back(self, arg):
        'Return to the main Goblin Extractor CLI.'
        return True



class GoblinExtractorCLI(cmd.Cmd):
    intro = "Welcome to the Goblin Extractor CLI. Type help or ? to list commands.\n"
    prompt = "(goblin-extractor) "

    def do_webscrape(self, arg):
        """Enter the Web Scraping CLI."""
        print("Entering Goblin Web Scraping CLI...")
        WebScraperSubCLI().cmdloop()

    def do_phonerecords(self, arg):
        'Enter the PhoneRecords CLI to manage CSV to JSON conversion and search.'
        print("Entering the Goblin phone records CLI")
        PhoneRecordsSubCLI().cmdloop()  

    def do_pdfextractor(self, arg):
        'Enter the PDF Extractor CLI.'
        print("Entering the PDF Extractor CLI...")
        PDFExtractorSubCLI().cmdloop()      

    def do_exit(self, arg):
        """Exit the Goblin Extractor CLI."""
        print("Exiting Goblin Extractor CLI.")
        return True

    # Placeholder for future functionalities
    def do_another_feature(self, arg):
        """Description of another feature (to be implemented)."""
        print("This feature is yet to be implemented.")

if __name__ == '__main__':
    GoblinExtractorCLI().cmdloop()
