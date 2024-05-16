import os
from lxml import etree
import re
import pandas as pd


def parse_xml(file_path, output_file):
    # Parse the XML file
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Define namespace map
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    types = ["court", "other", "running"]
    divs = []
    for type in types:
        divs = root.findall(f'.//tei:div[@type="{type}"]', ns)
        # divs.extend(found)
        for court in divs:
        # Extract information
            date = court.find('.//tei:date', ns)
            if date is not None:
                if 'when' in date.attrib:
                    date_val = date.get('when')
                elif 'notBefore' in date.attrib and 'notAfter' in date.attrib:
                    date_val = f"between {date.get('notBefore')} and {date.get('notAfter')}"
                elif 'from' in date.attrib and 'to' in date.attrib:
                    date_val = f"{date.get('from')}-{date.get('to')}"
                elif 'notBefore' in date.attrib:
                    date_val = date.get('notBefore')
                else:
                    date_val = "No date"
                date_cert = date.get('cert', "No cert")
            else:
                date_val = "No date"
                date_cert = "No cert"

            output_file.write(f"Date: {date_val}, Certification: {date_cert}\n\n")
            
            for div in court.findall('.//tei:div', ns):
                # entry_type = div.get('type')  # This is either 'heading' or 'entry'
                entry_id = div.get('{http://www.w3.org/XML/1998/namespace}id')
                entry_lang = div.get('{http://www.w3.org/XML/1998/namespace}lang')
                head = div.find('.//tei:head', ns) 
                
                # Process <head> if present
                head_text = process_element_text(head, ns)

                # Process paragraphs
                p_texts = [process_element_text(p, ns) for p in div.findall('.//tei:p', ns)]
                p_text = ' '.join(p_texts)

                
                if head is not None:
                    output_str = f"ID: {entry_id}  Language: {entry_lang}\nContent:\n{head_text}\n{p_text}\n\n"
                else:
                    output_str = f"ID: {entry_id}  Language: {entry_lang}\nContent:\n{p_text}\n\n"
                output_file.write(output_str)


def process_element_text(element, ns):
    texts = []
    if element is not None:
        if len(list(element)) > 0:
            for child in element.iterdescendants():
                child_text = etree.tostring(child, method='text', encoding='unicode').strip()
                pattern = re.compile(r'author=".*?" timestamp=".*?" comment=".*?"')
                cleaned_text = re.sub(pattern, ' ', child_text)
                if child.tag == "{http://www.tei-c.org/ns/1.0}lb" and child.get('break') == "yes":
                    texts.append(', ')
                    texts.append(cleaned_text)
                elif child.tag == "{http://www.tei-c.org/ns/1.0}lb" and child.get('break') == "no":
                    texts.append(cleaned_text)
                elif child.tag == "{http://www.tei-c.org/ns/1.0}unclear":
                    texts.append(cleaned_text)
                elif child.tag == "{http://www.tei-c.org/ns/1.0}supplied":
                    texts.append(cleaned_text)
                elif child.tag == "{http://www.tei-c.org/ns/1.0}gap":
                    texts.append("_" + cleaned_text) 
                elif child.tag == "{http://www.tei-c.org/ns/1.0}note":
                    continue
                elif child.tag == "{http://www.tei-c.org/ns/1.0}seg":
                    texts.append(cleaned_text)
                elif child.tag == "{http://www.tei-c.org/ns/1.0}expan":
                    texts.append(' ' +cleaned_text)
                else:
                    texts.append(cleaned_text)
        else:
            return element.text.strip() if element.text else ''

    return re.sub(r'\s+', ' ', ''.join(texts)).strip()


# Define function to process text files and save as CSV
def process_and_save_to_csv(file_path, output_csv_path):
    # Initialize an empty list to store parsed data
    data = []

    # Open and read file contents
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Match date and content blocks using regular expressions
        entries = re.split(r'Date: ', content)
        for entry in entries[1:]:  # Skip the first split result because it is empty
            date_section, rest = entry.split(',', 1)
            certification_section = rest.split('\n\nID: ', 1)[0].strip()
            date = date_section.strip()
            certification = certification_section.split(': ')[1].strip()

            # Split each record block
            records = re.split(r'\nID: ', rest)
            for record in records[1:]:  # Skip the first split result as it is already used to extract the date
                id_language_content = record.split('\nContent:\n', 1)
                # print(id_language_content)
                id_language = id_language_content[0].strip()
                # print(id_language)
                content = id_language_content[1].strip().replace('\n', ' ')
                # print(content)
                
                if ' Language: ' in id_language:
                    id, language = id_language.split(' Language: ')
                else:
                    id = id_language
                    language = 'unknown' 
                data.append([date, id, language, content, certification])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Date', 'ID', 'Language', 'Content', 'Certification'])

    # Save as CSV file
    df.to_csv(output_csv_path, index=False, encoding='utf-8')

directories = ['D:\CJ\course\大四下\\final project\ARO\XML files volumes 1-7', 'D:\CJ\course\大四下\\final project\ARO\XML files volume 8']

# Open a text file to write the output
with open('D:\CJ\course\大四下\\final project\ARO\parsed_xml.txt', 'w', encoding='utf-8') as output_file:
    for dir_path in directories:
        for file_name in os.listdir(dir_path):
            if file_name.endswith('.xml'):
                parse_xml(os.path.join(dir_path, file_name), output_file)


# Call the function to process the file and save it
process_and_save_to_csv('D:\CJ\course\大四下\\final project\ARO\parsed_xml.txt', 'D:\CJ\course\大四下\\final project\ARO\corpus.csv')
