import json
import sys
import os

def order_json_by_keywords(json_file, keywords):
    """
    Orders the entries in the provided JSON file based on the presence of keywords.

    Parameters:
    json_file (str): Name of the JSON file (without path).
    keywords (list): List of keywords to use for ordering.

    Returns:
    list: Ordered JSON data.
    """
    # Construct the full path to the JSON file in the data folder
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    json_path = os.path.join(data_folder, json_file)

    # Check if file exists
    if not os.path.exists(json_path):
        print(f"File {json_file} not found in the data folder.")
        return []

    # Load the JSON data from the file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Placeholder for ordering logic
    # Implement logic to order the data based on the provided keywords

    return data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ordering.py <json_file> <keyword1> <keyword2> ...")
        sys.exit(1)

    json_file = sys.argv[1] + '.json'  # Assume the file is given without an extension
    keywords = sys.argv[2:]

    ordered_data = order_json_by_keywords(json_file, keywords)

    # Print or save the ordered data
    if ordered_data:
        print(json.dumps(ordered_data, indent=2))
    else:
        print("Ordering failed or no data to display.")
