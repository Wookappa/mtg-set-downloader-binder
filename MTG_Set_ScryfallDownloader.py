import json  # Importing the JSON module for working with JSON data
import requests  # Importing the Requests module for making HTTP requests
import os  # Importing the OS module for working with files and directories
import re  # Importing the Regular Expression module for pattern matching and string manipulation
import datetime  # Importing the Datetime module for working with dates and times
import ijson  # Importing the ijson module for iterative JSON parsing
import urllib3  # Importing the urllib3 module for working with URLs
import urllib.request  # Importing the urllib.request module for making URL requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable SSL verification warning

def get_valid_filename(s):
    # Function to sanitize a string and make it a valid filename
    s = str(s).strip().replace(' ', '_')  # Strip leading/trailing whitespaces and replace spaces with underscores
    return re.sub(r'(?u)[^-\w.]', '', s)  # Remove any characters that are not alphanumeric, hyphen, or dot

def checkdir(dir_path):
    # Function to create a directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

def writefile(url, file_path):
    # Function to download a file from a given URL and save it to the specified file path
    if not os.path.isfile(file_path):  # Check if the file already exists
        r = requests.get(url, verify=False)  # Make an HTTP GET request to the URL (SSL verification disabled)
        with open(file_path, 'wb') as f:
            f.write(r.content)  # Write the response content to the file

def check_set_exists(set_code):
    # Function to check if a Magic: The Gathering set exists based on its set code
    url = f"https://api.scryfall.com/sets/{set_code}"  # API URL for the set
    response = requests.get(url)  # Make an HTTP GET request to the set URL

    if response.status_code == 200:
        return True  # The set exists
    else:
        return False  # The set does not exist

def get_all_cards_url(verify_ssl):
    # Function to get the URL for bulk data containing all Magic: The Gathering cards
    request_url = requests.get('https://api.scryfall.com/bulk-data', verify=verify_ssl)
    data = request_url.json()
    return data['data'][3]['download_uri']  # Return the download URL for the card data

def get_card_data_and_download(card_name, set_code, card_number, is_from_list=False):
    # Function to get card data from the Scryfall API and download the card image
    search_url = "https://api.scryfall.com/cards/search"
    set_code = set_code.replace("(", "").replace(")", "")  # Remove parentheses from the set code

    if set_code and card_number:
        query = f'name:"{card_name}" set:{set_code} number:{card_number}'  # Query string for searching the card
    else:
        query = f'name:"{card_name}"'  # Query string for searching the card without set code and card number

    params = {
        "q": query,
        "format": "json"
    }

    response = requests.get(search_url, params=params)  # Make an HTTP GET request to the search URL with the query

    if response.status_code == 200:
        data = response.json()

        if "data" in data and len(data["data"]) > 0:  # Check if card data is present
            card_data = data["data"][0]  # Get the first card data from the response
            saved, not_saved = save_card_image(card_data, is_from_list)  # Save the card image
        else:
            print(f"No card found for '{card_name}' in set '{set_code}' with number '{card_number}'")
    else:
        print(f"Error retrieving card data for '{card_name}' in set '{set_code}' with number '{card_number}'. Response: {response.text}")

    return saved, not_saved


def save_card_image(card, is_from_list=False):
    # Function to save the card image to the appropriate directory and file path
    set_name = get_valid_filename(card['set_name'])  # Sanitize the set name for the directory name
    if is_from_list:
        dir_path = os.path.join(output_dir, "CardsList")  # Output directory for card images when downloading from a list
    else:
        dir_path = os.path.join(output_dir, set_name)  # Output directory for card images when downloading a set
    checkdir(dir_path)  # Create the directory if it doesn't exist

    collector_number = get_valid_filename(card['collector_number'])  # Sanitize the collector number for the file name
    name = None
    file_path = None
    saved_count = 0
    not_saved_count = 0

    if 'image_uris' in card:
        name = get_valid_filename(card['name'])  # Sanitize the card name for the file name
        file_path = os.path.join(dir_path, f"{collector_number}_{name}.jpg")  # File path for the card image
    elif 'type_line' in card and card['type_line'] != 'Card // Card':
        if 'card_faces' in card and len(card['card_faces']) == 2:
            name = get_valid_filename(card['card_faces'][0]['name'])
            file_path_front = os.path.join(dir_path, f"{collector_number}_{name}_front.jpg")
            file_path_rear = os.path.join(dir_path, f"{collector_number}_{name}_rear.jpg")
    elif 'layout' in card and card['layout'] == 'reversible_card':
        if 'card_faces' in card and len(card['card_faces']) == 2:
            name = get_valid_filename(card['card_faces'][0]['name'])
            file_path_front = os.path.join(dir_path, f"{collector_number}_{name}_front.jpg")
            file_path_rear = os.path.join(dir_path, f"{collector_number}_{name}_rear.jpg")

    if file_path is not None:
        writefile(card['image_uris']['large'], file_path)  # Download and save the card image
        print(f"Card image saved: {file_path}")
        saved_count += 1
    elif file_path_front is not None and file_path_rear is not None:
        writefile(card['card_faces'][0]['image_uris']['large'], file_path_front)
        writefile(card['card_faces'][1]['image_uris']['large'], file_path_rear)
        print(f"Card images saved: {file_path_front}, {file_path_rear}")
        saved_count += 1
    else:
        print(f"No valid image found for card: {card['name']}")
        not_saved_count += 1

    return saved_count, not_saved_count

def download_cards_list(verify_ssl, is_from_list=False):
    # Function to download card images from a list of cards
    with open("cards.txt", "r") as file:
        card_list = file.readlines()  # Read the list of cards from a file

    saved_count = 0
    not_saved_count = 0

    for card in card_list:
        card_data = card.strip().split(" ")  # Split the card data into card name, set code, and card number

        if len(card_data) < 3:
            card_name = card.strip()
            set_code = ""
            card_number = ""
        else:
            card_name = " ".join(card_data[:-2])
            set_code = card_data[-2]
            card_number = card_data[-1]

        saved, not_saved = get_card_data_and_download(card_name, set_code, card_number, is_from_list)
        saved_count += saved
        not_saved_count += not_saved

    print(f"Total cards saved: {saved_count}")
    print(f"Total cards not saved: {not_saved_count}")

def download_set(verify_ssl):
    # Function to download card images from a specific Magic: The Gathering set
    set_code = input("Enter the set code (e.g., 'ltr'): ")  # Prompt the user to enter the set code

    with urllib.request.urlopen(get_all_cards_url(verify_ssl)) as f:
        objects = ijson.items(f, 'item')  # Iterate over the JSON objects in the data stream

        cards = (o for o in objects if o['set'] == set_code and o['lang'] == 'en')  # Filter cards for the specified set code and English language
        if check_set_exists(set_code):
            saved_count = 0
            not_saved_count = 0
            for card in cards:
                saved, not_saved = save_card_image(card)  # Save the card image
                saved_count += saved
                not_saved_count += not_saved
            print(f"Total cards saved: {saved_count}")
            print(f"Total cards not saved: {not_saved_count}")
        else:
            print("Unable to find the URL for set data", set_code)

start = datetime.datetime.now()  # Get the current date and time
output_dir = os.path.join(os.getcwd(), "art")  # Output directory for card images
print("Writing files to", output_dir)

print("Starting at:", start)
option = input("Choose an option:\n1. Download a set\n2. Download cards from a list\nEnter option number (1 or 2): ")

verify_ssl = input("Verify SSL (True/False): ").lower() == 'true'  # Prompt the user to enter whether to verify SSL

if option == '1':
    download_set(verify_ssl)  # Download a set
elif option == '2':
    download_cards_list(verify_ssl, is_from_list=True)  # Download cards from a list

end = datetime.datetime.now()  # Get the current date and time after the execution
elapsed_time = end - start  # Calculate the elapsed time
print("Finished at", end, ". Elapsed time:", elapsed_time)
