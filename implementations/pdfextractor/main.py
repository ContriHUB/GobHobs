import subprocess
import os
import sys
import json

# Define paths for the data and results folders
data_folder = os.path.join(os.path.dirname(__file__), 'data')
results_folder = os.path.join(os.path.dirname(__file__), 'results')
pdf_extract_python = os.path.join(os.path.dirname(__file__), 'extractfrompdf.py')
pdf_extract_js = os.path.join(os.path.dirname(__file__), 'extractfrompdf.js')

def extract_data_from_pdf(pdf_filename):
    """
    Extract structured data from a PDF using Python or JavaScript implementations.
    """

    # Check if the PDF file exists
    pdf_path = os.path.join(data_folder, pdf_filename + '.pdf')
    if not os.path.exists(pdf_path):
        return "File Not Found"

    # Try using the Python implementation first
    try:
        result = subprocess.check_output(['python', pdf_extract_python, pdf_filename])
        if "not implemented" in result.decode('utf-8').lower():
            raise subprocess.CalledProcessError(1, "Python implementation not implemented.")
        return "Python Implementation Success"
    except subprocess.CalledProcessError:
        print("Python implementation not implemented or failed. Trying JavaScript...")

    # If Python fails, try the JavaScript implementation
    try:
        result = subprocess.check_output(['node', pdf_extract_js, pdf_filename])
        if "not implemented" in result.decode('utf-8').lower():
            raise subprocess.CalledProcessError(1, "JavaScript implementation not implemented.")
        return "JavaScript Implementation Success"
    except subprocess.CalledProcessError:
        print("JavaScript implementation not implemented or failed.")
        return "Not Implemented"

def view_json_data(json_filename):
    """
    View JSON data from the results folder.
    """
    json_path = os.path.join(results_folder, json_filename + '.json')

    if not os.path.exists(json_path):
        return f"Error: The file {json_filename}.json does not exist in the results folder."

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return json.dumps(data, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <command> <filename>")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "extract":
        result = extract_data_from_pdf(filename)
        if result == "File Not Found":
            print(f"Error: The file {filename}.pdf does not exist in the data folder.")
        elif result == "Not Implemented":
            print("Extraction functionality not implemented in either Python or JavaScript.")
        else:
            print(f"Success: {filename}.json has been created in the results folder.")
    elif command == "view":
        result = view_json_data(filename)
        print(result)
    else:
        print("Invalid command. Use 'extract' to extract data or 'view' to view JSON data.")
