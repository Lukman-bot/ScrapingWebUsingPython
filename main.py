import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import sys

# Array URL
urls = [
    'https://meionovel.id/novel/86-ln/volume-4-chapter-0',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-1',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-2',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-3',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-4',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-5',
    'https://meionovel.id/novel/86-ln/volume-4-chapter-6',
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

        return True
    except requests.exceptions.RequestException as e:
        return False

# Main loop to process URLs
timeout_duration = 15
for url in urls:
    retry_attempts = 0
    while True:
        if fetch_and_save_content(url, timeout_duration):
            print(f'Berhasil menyimpan konten dari {url}')
            break
        else:
            retry_attempts += 1
            print(f'Gagal mengambil halaman web {url}. Menyambungkan ulang... (Percobaan {retry_attempts})')
            with tqdm(total=10, desc=f"Retrying {url}", bar_format='{l_bar}{bar}| [{elapsed}<{remaining}]', leave=False, colour='red') as retry_bar:
                for _ in range(10):
                    time.sleep(1)
                    retry_bar.update(1)
            print('\r', end='')  # Clear the retry message after successful retry
            sys.stdout.flush()
