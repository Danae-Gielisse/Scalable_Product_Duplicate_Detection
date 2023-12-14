import json
import pandas as pd
import re

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise IOError(f"Error reading file: {e}")

def print_first_4_items_in_dictionary(dict):
    for key, value in list(dict.items())[:4]:
        print(f"Key: {key}, Value: {value}")

def get_title(dict):
    titles_dict = {}
    for key, value in dict.items():
        for item in value:
            titles_dict[key] = item['title']

    return titles_dict

def dictionary_to_dataframe(dictionary):
    rows = []
    for key, value in dictionary.items():
        for item in value:
            row = {
                'Key': key,
                'Shop': item['shop'],
                'URL': item['url'],
                'ModelID': item['modelID'],
                'Title': item['title']
            }

            # Add the featuresmap
            row.update(item['featuresMap'])
            rows.append(row)

    df = pd.DataFrame(rows)
    return df

def extract_titles(product_list, titles_list_processed):
    result_dict = dict(zip(product_list, titles_list_processed))
    return result_dict


# Pre process the titles
def pre_process(titles_list):
    processed_titles_list = []

    for title in titles_list:
        # convert titles to lowercase
        for word in title:
            title = title.replace(word, word.lower())
        # Replace ".0" following a number with an empty string
            title = re.sub(r'(\d+)\.0\b', r'\1', title)
        # remove certain characters
        characters = ['/', "(", ")", " -"]
        for word in characters:
            if word in title:
                title = title.replace(word, "")
        # convert all hertz instanced to hz
        hz_list = ['hertz', 'hz', ' hz', '-hz', ' hertz']
        for word in hz_list:
            if word in titles_list:
                title = title.replace(word, 'hz')
        # convert all inch instances to inch
        inch_list = [' inch', 'inches', '-inch', '"', 'inch', ' inches']
        for word in inch_list:
            if word in inch_list:
                title = title.replace(word, 'inch')
        # delete - in led-lcd
        if 'led-lcd' in title:
            title = title.replace('led-lcd', "ledlcd")
        # delete characters and store names
        words = ['/', "(", ")", " -", "newegg.com ", "thenerds.net ", "best buy ", "tv", "class", ";", "$"]
        for word in words:
            if word in title:
                title = title.replace(word, "")
        # remove all variants of diagonal
        typeDiagonal = ['diag.', ' diag.' ' diagonally', ' diagonal widescreen', ' diagonal size', ' diag', 'diag', 'diagonal', ' diagonal', 'diagonal size']
        for word in typeDiagonal:
            if word in title:
                title = title.replace(word, "")
        processed_titles_list.append(title)

    return processed_titles_list


def pre_process_less_cleaning(titles_list):
    processed_titles_list = []

    for title in titles_list:
        # convert titles to lowercase
        for word in title:
            title = title.replace(word, word.lower())
        # convert all hertz instanced to hz
        hz_list = ['hertz', 'hz', ' hz', '-hz', ' hertz']
        for word in hz_list:
            if word in titles_list:
                title = title.replace(word, 'hz')
        # convert all inch instances to inch
        inch_list = [' inch', 'inches', '-inch', '"', 'inch', ' inches']
        for word in inch_list:
            if word in inch_list:
                title = title.replace(word, 'inch')
        processed_titles_list.append(title)

    return processed_titles_list