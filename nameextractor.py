import os
import fitz  # PyMuPDF
import shutil


def find_largest_text_in_first_two_pages(doc):
    largest_text = ""
    largest_size = 0
    # Process the first two pages or the total number of pages if less than two
    for page_num in range(min(2, len(doc))):
        page = doc[page_num]
        text_instances = page.get_text("dict")["blocks"]
        for instance in text_instances:
            if "lines" in instance:
                for line in instance["lines"]:
                    for span in line["spans"]:
                        # Check if the text length is at least 20 characters
                        if span["size"] > largest_size and len(span["text"]) >= 30:
                            largest_size = span["size"]
                            largest_text = span["text"]
    return largest_text

def sanitize_filename(title):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '')
    return title

def rename_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):          
            pdf_path = os.path.join(directory, filename)
            try:
                doc = fitz.open(pdf_path)
                title = find_largest_text_in_first_two_pages(doc).strip().replace("/", "-")  # Basic sanitization
                doc.close()
                title = sanitize_filename(title)
                if title:
                    new_filename = title + ".pdf"
                    new_path = os.path.join(directory, new_filename)
                    os.rename(pdf_path, new_path)          
                else:
                    print(f"Could not extract title for '{filename}'")
                doc.close()
            except Exception as e:
                print(f"Error processing '{filename}': {e}")



directory_path = './'
rename_pdfs_in_directory(directory_path)
