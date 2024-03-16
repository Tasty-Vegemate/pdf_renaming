import os
import fitz  # PyMuPDF


def find_largest_text_in_first_two_pages(doc):
    size_text_list = []
    doc = fitz.open(doc)
    largest_size = 0
    for page_num in range(min(2, len(doc))):
        page = doc[page_num]
        text_instances = page.get_text("dict")["blocks"]
        for instance in text_instances:
            if "lines" in instance:
                for line in instance["lines"]:
                    for span in line["spans"]:
                        if span["size"] > largest_size:
                            largest_size = span["size"]
                            number = instance["number"]
                            text = span["text"]
                            size_text_list.append({"page_number" : page_num , "number" : number, "text": [text]})
                            
            if number == instance["number"]:
                for line in instance["lines"]:
                    for span in line["spans"]:
                        text_add = span["text"]
                        if text_add != text:
                            for item in size_text_list:
                                if item["page_number"] == page_num and item["number"] == number:
                                    item["text"][-1] += f" {text_add}"
    max_length = 0
    for item in size_text_list:
        text_length = len(item['text'][0])
        if text_length > max_length:
            max_length = text_length
            title = item["text"][0]
    doc.close()
    return title

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
                title = sanitize_filename(title)
                doc.close()
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
