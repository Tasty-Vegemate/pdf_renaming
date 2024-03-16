import fitz

def number_size_extracter(location):
    size_text_list = []
    doc = fitz.open(location)
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
            Title = item["text"][0]

    return Title






Title = number_size_extracter("./s41467-021-26511-5.pdf")
print(Title)