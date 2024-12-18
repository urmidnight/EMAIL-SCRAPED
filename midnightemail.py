from collections import deque
import re
from bs4 import BeautifulSoup
import requests  # Perbaikan pada 'request' menjadi 'requests'
import urllib.parse  # Perbaikan pada 'urlib' menjadi 'urllib'

# Memasukkan URL awal
user_url = str(input('[+] Masukkan URL: '))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while True:
        count += 1
        if count > 10:
            break  # Batasi proses hanya pada 10 URL

        # Ambil URL dari antrian
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        print(f'{count} Memproses {url}')
        
        try:
            # Kirim permintaan HTTP GET
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # Jika terjadi kesalahan pada URL, lewati
            continue

        # Cari email di halaman
        new_emails = set(re.findall(r'[a-z0-9.\+-_]+@[a-z0-9\.-]+\.[a-z]+', response.text, re.I))
        emails.update(new_emails)

        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link  # Tambahkan domain ke link relatif
            elif not link.startswith('http'):
                link = path + link  # Tambahkan path ke link relatif
            
            # Tambahkan link ke antrian jika belum diproses
            if link not in urls and link not in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('\n[-] Proses dihentikan oleh pengguna.')

print('\nProses selesai!')
print(f'\n{len(emails)} email ditemukan:\n==============================')

# Cetak semua email yang ditemukan
for mail in emails:
    print(' ' + mail)
print('\n')

