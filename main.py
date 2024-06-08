import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import sys
import os
from colorama import Fore, Style, init

# Initialize colorama
init()

# Array URL
urls = [
    'https://meionovel.id/novel/saikyou-mahoushi-no-inton-keikaku-ln/volume-10-chapter-3',
]

# Function for clean filename
def clean_filename(text):
    translation_table = str.maketrans('', '', '?,!/=+:')
    return text.translate(translation_table)

# Function to fetch and save content with a simulated progress bar
def fetch_and_save_content(url, timeout_duration):
    try:
        print(Fore.YELLOW + f"Fetching {url}" + Style.RESET_ALL)
        # Simulate the fetch process with a progress bar based on the timeout duration
        with tqdm(total=timeout_duration, desc="Fetching", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]', leave=False) as fetch_progress:
            response = requests.get(url, timeout=timeout_duration)
            response.raise_for_status()
            for _ in range(timeout_duration):
                time.sleep(1)
                fetch_progress.update(1)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        li_element = soup.find('li', class_='active')
        if li_element:
            li_text = li_element.get_text().strip()
        else:
            li_text = 'Untitled'

        # Clean the filename
        filename = f"{clean_filename(li_text)}.txt"

        div_elements = soup.find_all('div', class_='text-left')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(li_text + '\n')
            for element in div_elements:
                inner_html = element.decode_contents()
                file.write(inner_html + '\n')

        return filename
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}" + Style.RESET_ALL)
        return None

# Function to upload file with a simulated progress bar
def upload_file(file_path, url, id_pengguna, id_light_novel):
    try:
        print(Fore.YELLOW + f"Uploading {file_path}" + Style.RESET_ALL)
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {'id_pengguna': id_pengguna, 'id_light_novel': id_light_novel}

            with tqdm(total=1, desc="Uploading", leave=False) as pbar:
                response = requests.post(url, files=files, data=data)
                pbar.update(1)

            response.raise_for_status()

            # Print response message from the endpoint
            response_json = response.json()
            print(Fore.GREEN + response_json.get("message", "No message in response") + Style.RESET_ALL)

            return True
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            try:
                error_json = e.response.json()
                if e.response.status_code == 422:
                    message = error_json.get('message', 'Unknown error')
                    if isinstance(message, dict):
                        for key, value in message.items():
                            print(Fore.RED + f"Error: {value[0]}" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"Error: {message}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Error:" + e.response.text + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Error: Failed to parse error response" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Error: Unable to connect to the server. Please check the server status and try again." + Style.RESET_ALL)
        return False

# Main loop to process URLs
timeout_duration = 15
upload_url = 'http://lukman.com/otakucode/v3/adm.novel/api/light-novel/import-txt'
id_pengguna = '5'
id_light_novel = '35'

for url in urls:
    retry_attempts = 0
    while retry_attempts < 3:
        filename = fetch_and_save_content(url, timeout_duration)
        if filename:
            if upload_file(filename, upload_url, id_pengguna, id_light_novel):
                print(Fore.GREEN + f"Upload successful for {filename}" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + f"Upload failed for {filename}. Retrying..." + Style.RESET_ALL)
                retry_attempts += 1
        else:
            print(Fore.RED + f'Failed to fetch web page {url}. Retrying... (Attempt {retry_attempts + 1})' + Style.RESET_ALL)
            retry_attempts += 1
        
        print(Fore.YELLOW + f"Retrying {url}" + Style.RESET_ALL)
        with tqdm(total=10, desc="Retrying", bar_format='{l_bar}{bar}| [{elapsed}<{remaining}]', leave=False, colour='red') as retry_bar:
            for _ in range(10):
                time.sleep(1)
                retry_bar.update(1)
    else:
        print(Fore.RED + f"Failed to process {url} after {retry_attempts} attempts. Exiting." + Style.RESET_ALL)
        sys.exit(1)
