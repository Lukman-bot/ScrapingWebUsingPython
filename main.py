import requests
from bs4 import BeautifulSoup

url = 'https://meionovel.id/novel/maou-gakuin-no-futekigousha/volume-3-chapter-1'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    li_element = soup.find('li', class_='active')
    if li_element:
        li_text = li_element.get_text().strip()
    else:
        li_text = 'Untitled'

    div_elements = soup.find_all('div', class_='text-left')
    filename = f"{li_text}.txt"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(li_text + '\n')
        
        for element in div_elements:
            inner_html = element.decode_contents()
            file.write(inner_html + '\n')

    print(f'Data berhasil disimpan ke {filename}')
else:
    print('Gagal mengambil halaman web. Kode status:', response.status_code)
