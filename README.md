# Scraping Web Menggunakan Python

Kode Python ini dirancang untuk melakukan scraping konten dari serangkaian URL yang tercantum dalam array `urls`. Ini mengambil konten HTML dari setiap URL, mengekstrak informasi yang relevan menggunakan BeautifulSoup, dan menyimpan konten ke file teks. Jika koneksi time out atau terjadi kesalahan selama pengambilan, skrip akan mencoba lagi.

## Instalasi

1. **Clone Repository:** Clone repository ini ke mesin lokal Anda menggunakan perintah berikut:

2. **Instal Dependensi:** Buka direktori proyek dan instal dependensi yang diperlukan menggunakan pip:
```bash
pip install requests bs4 tqdm
```


## Penggunaan

1. **Jalankan Skrip:** Jalankan skrip `main.py` menggunakan interpreter Python. Pastikan Anda berada di dalam direktori proyek:
```bash
python main.py
```

2. **Lihat Output:** Setelah skrip dijalankan, itu akan melakukan scraping konten dari URL yang ditentukan dan menyimpannya ke file teks. Anda dapat menemukan file teks yang disimpan di direktori yang sama dengan skrip.

## Penyesuaian

- **URLs:** Anda dapat menyesuaikan daftar URL yang akan di-scrape dengan memodifikasi array `urls` dalam skrip `main.py`.
- **Durasi Time Out:** Durasi time out untuk setiap pengambilan URL diatur ke 15 detik secara default (`timeout_duration = 15`). Anda dapat menyesuaikan nilai ini berdasarkan kebutuhan Anda.
- **Percobaan Ulang:** Skrip secara otomatis mencoba kembali pengambilan jika mengalami kesalahan. Secara default, skrip mencoba kembali 10 kali, menunggu 1 detik antara setiap percobaan. Anda dapat menyesuaikan parameter ini sesuai kebutuhan.

