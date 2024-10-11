import os
import json
import pdfplumber
import fitz  # PyMuPDF

def extract_data_from_pdf(pdf_filename):
    """
    Extract structured data from the given PDF file (e.g., tables, key-value pairs).
    """
    # Define the path to the PDF file in the 'data' folder
    pdf_path = os.path.join(os.path.dirname(__file__), 'data', pdf_filename + '.pdf')

    extracted_data = {
        "bodyText": "",
        "tables": [],
        "images": extract_images_from_pdf(pdf_filename),
    }

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text from the page
            text = page.extract_text()
            if text:
                extracted_data["bodyText"] += text
            
            # Extract tables from the page (if any)
            tables = page.extract_tables()
            if tables:
                extracted_data["tables"].extend(tables)
    
    return extracted_data

def extract_images_from_pdf(pdf_filename):
    # Create the 'results/images/' folder if it does not exist
    images_folder = os.path.join(os.path.dirname(__file__), 'results', 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    pdf_path = os.path.join(os.path.dirname(__file__), 'data', pdf_filename + '.pdf')
    pdf_document = fitz.open(pdf_path)
    image_data = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            try:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Save the image in 'results/images/' folder
                img_filename = f"{pdf_filename}_page{page_num + 1}_img{img_index + 1}.{image_ext}"
                img_filepath = os.path.join(images_folder, img_filename)

                with open(img_filepath, 'wb') as img_file:
                    img_file.write(image_bytes)

                # Store image metadata
                image_data.append({
                    "page": page_num + 1,
                    "img_index": img_index + 1,
                    "file_path": img_filepath,
                })

            except Exception as e:
                print(f"Error processing page {page_num}, image {img_index}: {e}")

    return image_data

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python extractfrompdf.py <pdf_filename>")
        sys.exit(1)

    pdf_filename = sys.argv[1]
    extracted_data = extract_data_from_pdf(pdf_filename)

    # Save the extracted data to a JSON file
    output_path = os.path.join(os.path.dirname(__file__), 'results', pdf_filename + '.json')
    with open(output_path, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"Extracted data saved to {output_path}")
