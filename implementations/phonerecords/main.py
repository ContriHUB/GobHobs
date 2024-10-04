import json
import os
import sys
import csv
import subprocess
from searchrecords import search_records as py_search_records

def create_json(csv_filename):
    # Ensure paths are correct
    samplecsv_path = os.path.join(os.path.dirname(__file__), 'samplecsv', csv_filename)

    if not os.path.exists(samplecsv_path):
        print(f"Error: The file {csv_filename} does not exist in the samplecsv folder.")
        sys.exit(1)

    data = []
    
    # Read the CSV file and convert it to JSON
    with open(samplecsv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    json_filename = f"{os.path.splitext(csv_filename)[0]}.json"
    json_path = os.path.join(os.path.dirname(__file__), 'data', json_filename)

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)

    print(f"Data successfully converted to JSON and saved to {json_path}")



data_folder = os.path.join(os.path.dirname(__file__), 'data')
js_search_script = os.path.join(os.path.dirname(__file__), 'searchrecords.js')

def search_records_in_file(json_filename, field_index, search_term):
    """
    Search for records in the JSON file using either Python or JavaScript search logic.
    """

    # Check if the JSON file exists in the 'data' folder
    json_path = os.path.join(data_folder, json_filename + '.json')
    if not os.path.exists(json_path):
        return "File Not Found", [], []

    # First, try the Python implementation
    exact_matches, like_matches = py_search_records(json_filename, field_index, search_term)
    
    if not exact_matches and not like_matches:
        # If Python implementation returns empty, try the JavaScript implementation
        try:
            result = subprocess.check_output(['node', js_search_script, json_filename, str(field_index), search_term])

            # Check if result is empty or invalid
            if not result.strip():
                print("JavaScript search returned empty. Assuming not implemented.")
                return "Not Implemented", [], []

            # Decode the byte output and parse the JSON
            result = result.decode('utf-8')
            result = json.loads(result)

            # Extract exactMatches and likeMatches from the result
            exact_matches = result.get('exactMatches', [])
            like_matches = result.get('likeMatches', [])

        except subprocess.CalledProcessError as e:
            print(f"JavaScript search failed: {str(e)}. Assuming not implemented.")
            return "Not Implemented", [], []
        except FileNotFoundError:
            print("Node.js or searchrecords.js not found.")
            return "Not Implemented", [], []
        except json.JSONDecodeError as e:
            print(f"Invalid JSON returned by JavaScript search: {str(e)}. Assuming not implemented.")
            return "Not Implemented", [], []

    # If still empty, return that the search functionality is not implemented
    if not exact_matches and not like_matches:
        print("Search functionality not implemented in both Python and JavaScript.")
        return "Not Implemented", [], []

    return "Implemented", exact_matches, like_matches



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args...]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "createjson":
        if len(sys.argv) != 3:
            print("Usage: python main.py createjson <csv_filename>")
            sys.exit(1)
        create_json(sys.argv[2])
    elif command == "search":
        json_filename = sys.argv[2]
        field_index = int(sys.argv[3])
        search_term = sys.argv[4]

        # Check if the file exists before proceeding with the search
        status, exact_matches, like_matches = search_records_in_file(json_filename, field_index, search_term)

        if status == "File Not Found":
            print(json.dumps({"error": f"Error: The file {json_filename}.json does not exist in the data folder."}, indent=2))
        elif status == "Not Implemented":
            print(json.dumps({"error": "Search functionality not implemented yet."}, indent=2))
        else:
            result = {
                "exact_matches": exact_matches,
                "like_matches": like_matches
            }
            print(json.dumps(result, indent=2))
    else:
        print("Invalid command.")
