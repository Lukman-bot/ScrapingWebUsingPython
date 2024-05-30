import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import sys

# Array URL
urls = [
    'https://meionovel.id/novel/toaru-majutsu-no-index-genesis-testament-ln/mtl/volume-1-chapter-1',
    'https://meionovel.id/novel/toaru-majutsu-no-index-genesis-testament-ln/mtl/volume-1-chapter-2',
]

# Function for clean filename
def clean_filename(text):
    translation_table = str.maketrans('', '', '?,!/=+:')
    return text.translate(translation_table)

# Function to fetch and save content with a simulated progress bar
def fetch_and_save_content(url, timeout_duration):
    try:
        # Simulate the fetch process with a progress bar based on the timeout duration
        with tqdm(total=timeout_duration, desc=f"Fetching {url}", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]', leave=False) as fetch_progress:
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
        return None

# Function to upload file with a simulated progress bar
def upload_file(file_path, url, id_pengguna, id_light_novel):
    try:
        files = {'file': open(file_path, 'rb')}
        data = {'id_pengguna': id_pengguna, 'id_light_novel': id_light_novel}

        with tqdm(total=1, desc=f"Uploading {file_path}", leave=False) as pbar:
            response = requests.post(url, files=files, data=data)
            pbar.update(1)

        response.raise_for_status()

        # Print response message from the endpoint
        response_json = response.json()
        print(response_json.get("message", "No message in response"))

        return True
    except requests.exceptions.RequestException as e:
        try:
            error_json = e.response.json()
            if e.response.status_code == 422:
                message = error_json.get('message', 'Unknown error')
                if isinstance(message, dict):
                    for key, value in message.items():
                        print(f"Error: {value[0]}")
                else:
                    print(f"Error: {message}")
            else:
                print("Error:", e.response.text)
        except ValueError:
            print("Error: Failed to parse error response")
        return False
    finally:
        files['file'].close()

# Main loop to process URLs
timeout_duration = 15
for url in urls:
    retry_attempts = 0
    while True:
        filename = fetch_and_save_content(url, timeout_duration)
        if filename:
            upload_url = 'http://127.0.0.1:8000/api/light-novel/import-txt'
            id_pengguna = '1'
            id_light_novel = '15'
            
            if upload_file(filename, upload_url, id_pengguna, id_light_novel):
                break
            else:
                sys.exit(1)
        else:
            retry_attempts += 1
            print(f'Gagal mengambil halaman web {url}. Menyambungkan ulang... (Percobaan {retry_attempts})')
        
        with tqdm(total=10, desc=f"Retrying {url}", bar_format='{l_bar}{bar}| [{elapsed}<{remaining}]', leave=False, colour='red') as retry_bar:
            for _ in range(10):
                time.sleep(1)
                retry_bar.update(1)
        print('\r', end='')  # Clear the retry message after successful retry
        sys.stdout.flush()
