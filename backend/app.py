from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

# Route for web scraping
@app.route('/webscrape', methods=['POST'])
def webscrape():
    query = request.json['query']
    output_file = request.json['output_file']  # Get the output filename

    try:
        # Call the main.py web scraping function
        result = subprocess.check_output(['python', '../implementations/webscraping/main.py', query, output_file])
        
        # Assume the output is in the correct format
        return jsonify({"result": result.decode('utf-8')})

    except subprocess.CalledProcessError as e:
        # Handle the case where the web scraping process fails
        return jsonify({"error": f"Web scraping failed: {str(e)}"}), 500

    except Exception as e:
        # Catch any other exceptions
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route for ordering data
@app.route('/order', methods=['POST'])
def order():
    filename = request.json['filename']  # JSON file to order
    keywords = request.json['keywords']  # List of keywords

    # Call the order function in main.py
    try:
        result = subprocess.check_output(['python', '../implementations/webscraping/main.py', filename, *keywords])
        return jsonify({"result": result.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/createjson', methods=['POST'])
def create_json():
    data = request.json
    if 'csv_filename' not in data:
        return jsonify({"error": "Missing 'csv_filename' in request"}), 400

    csv_filename = data['csv_filename'] + ".csv"

    try:
        # Call the main.py function in phonerecords folder to create JSON
        result = subprocess.check_output(['python', '../implementations/phonerecords/main.py', 'createjson', csv_filename])

        return jsonify({"message": f"CSV file {csv_filename} successfully converted to JSON"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# Route for searching records
@app.route('/search', methods=['POST'])
def search():
    filename = request.json['filename']  # Only the filename, no path
    field = request.json['field']
    search_term = request.json['search_term']

    try:
        # Call the main.py search function in phonerecords
        result = subprocess.check_output(['python', '../implementations/phonerecords/main.py', 'search', filename, str(field), search_term])
        return jsonify({"result": result.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



# Route for extracting data from a PDF
@app.route('/extractpdf', methods=['POST'])
def extract_pdf():
    data = request.json
    if 'filename' not in data:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    pdf_filename = data['filename']

    try:
        # Call the main.py extract function
        result = subprocess.check_output(['python', '../implementations/pdfextractor/main.py', 'extract', pdf_filename])
        return jsonify({"message": result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Extraction failed: {str(e)}"}), 500

# Route for viewing JSON data
@app.route('/viewjson', methods=['POST'])
def view_json():
    data = request.json
    if 'filename' not in data:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    json_filename = data['filename']

    try:
        # Call the main.py view function
        result = subprocess.check_output(['python', '../implementations/pdfextractor/main.py', 'view', json_filename])
        return jsonify({"data": result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Viewing JSON failed: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)
