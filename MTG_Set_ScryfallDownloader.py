import json
import requests
import os
import re
import datetime
import ijson
import urllib.request

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def checkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

def writefile(url, file_path):
    if not os.path.isfile(file_path):
        r = requests.get(url, verify=False)
        with open(file_path, 'wb') as f:
            f.write(r.content)

def check_set_exists(set_code):
    url = f"https://api.scryfall.com/sets/{set_code}"
    response = requests.get(url)

    if response.status_code == 200:
        return True  # The set exists
    else:
        return False  # The set does not exist

def get_all_cards_url():
    request_url = requests.get('https://api.scryfall.com/bulk-data', verify=verify_ssl)
    data = request_url.json()
    return data['data'][3]['download_uri']

start = datetime.datetime.now()
output_dir = os.path.join(os.getcwd(), "art")
print("Writing files to", output_dir)

print("Starting at:", start)
set_code = input("Enter the set code (e.g., 'ltr'): ")
verify_ssl = input("Verify SSL (True/False): ").lower() == 'true'

with urllib.request.urlopen(get_all_cards_url()) as f:
    objects = ijson.items(f, 'item')

    cards = (o for o in objects if o['set'] == set_code and o['lang'] == 'en')
    if check_set_exists(set_code):
        for card in cards:
            set_name = get_valid_filename(card['set_name'])
            dir_path = os.path.join(output_dir, set_name)
            checkdir(dir_path)

            if 'image_uris' in card:
                collector_number = get_valid_filename(card['collector_number'])
                name = get_valid_filename(card['name'])
                file_path = os.path.join(dir_path, f"{collector_number}_{name}.jpg")
                writefile(card['image_uris']['large'], file_path)
            else:
                if 'type_line' in card and card['type_line'] != 'Card // Card':
                    collector_number = get_valid_filename(card['collector_number'])
                    name = get_valid_filename(card['card_faces'][0]['name'])
                    file_path_front = os.path.join(dir_path, f"{collector_number}_{name}_front.jpg")
                    file_path_rear = os.path.join(dir_path, f"{collector_number}_{name}_rear.jpg")
                    writefile(card['card_faces'][0]['image_uris']['large'], file_path_front)
                    writefile(card['card_faces'][1]['image_uris']['large'], file_path_rear)
                elif 'layout' in card and card['layout'] == 'reversible_card':
                    collector_number = get_valid_filename(card['collector_number'])
                    name = get_valid_filename(card['card_faces'][0]['name'])
                    file_path_front = os.path.join(dir_path, f"{collector_number}_{name}_front.jpg")
                    file_path_rear = os.path.join(dir_path, f"{collector_number}_{name}_rear.jpg")
                    writefile(card['card_faces'][0]['image_uris']['large'], file_path_front)
                    writefile(card['card_faces'][1]['image_uris']['large'], file_path_rear)
    else:
        print("Unable to find the URL for set data", set_code)
end = datetime.datetime.now()
elapsed_time = end - start
print("Finished at", end, ". Elapsed time:", elapsed_time)
