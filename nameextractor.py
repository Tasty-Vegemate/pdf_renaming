import os
import fitz  # PyMuPDF
import shutil

def find_largest_text_on_first_page(doc):
    first_page = doc[0]
    text_instances = first_page.get_text("dict")["blocks"]
    largest_text = ""
    largest_size = 0
    for instance in text_instances:
        if "lines" in instance:
            for line in instance["lines"]:
                for span in line["spans"]:
                    if span["size"] > largest_size:
                        largest_size = span["size"]
                        largest_text = span["text"]
    return largest_text

def rename_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):          
            pdf_path = os.path.join(directory, filename)
            try:
                doc = fitz.open(pdf_path)
                title = find_largest_text_on_first_page(doc).strip().replace("/", "-")  # Basic sanitization
                doc.close()
                if title:
                    new_filename = title + ".pdf"
                    new_path = os.path.join(directory, new_filename)
                    os.rename(pdf_path, new_path)          
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Could not extract title for '{filename}'")
                doc.close()
            except Exception as e:
                print(f"Error processing '{filename}': {e}")



directory_path = './'
rename_pdfs_in_directory(directory_path)
