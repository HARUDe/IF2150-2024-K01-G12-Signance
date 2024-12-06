![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# Signance
> Additional information or tagline

Perangkat lunak Signance adalah sebuah aplikasi pengelola keuangan pribadi. Pengguna dapat menambahkan, mengubah, melihat, dan menghapus riwayat transaksi. Pengguna dapat melakukan filtrasi pada daftar riwayat transaksi berdasarkan kriteria tertentu untuk mempermudah pencarian. Pengguna dapat menambahkan, mengubah, melihat, dan menghapus tabungan, yaitu target  yang ingin dicapai dalam kurun waktu tertentu. Pengguna dapat menambahkan, mengubah, melihat, dan menghapus anggaran, yaitu rencana pengeluaran pengguna pada suatu kategori dalam kurun waktu tertentu.

## Installing / Getting started

Ikuti Langkah ini untuk nge-run aplikasi

1. pip install PyQt5 di terminal
2. copy and paste "python src/main.py" ke terminal


## Modul

#### Nama Modul
1. Lorem ipsum
2.
3.

#### Pembagian Tugas
| Name                               |   Modul    |
|------------------------------------|------------|
|       Mochammad Fariz Rifqi R      |  |
|       Muhammad Jibril Ibrahim      |  |
|       Darrel Adinarya Sunanda      |  |
|   Muhammad Hazim Ramadhan Prajoda  |  |

#### Screenshot

-----

## Daftar Tabel Basis Data

-----

## Tujuan masing-masing directory di dalam src

1. src/views/ - Semua implementasi UI PyQt :
- main_window.py - Jendela utama aplikasi.
- /pages/ - Implementasi layar individu (login, dashboard, dll.).
- /components/ - Widget PyQt yang dapat digunakan kembali dan elemen UI. 
    
2. src/models/ - Struktur data dan objek bisnis :
- Mendefinisikan kelas-kelas yang merepresentasikan data Anda (User, Transaction, dll.).
- Tidak ada kode UI di sini.

3. src/controllers/ - Logika bisnis :
- Mengelola interaksi antara views dan models.
- Berisi logika aplikasi.
- Tidak ada kode UI di sini.

4. src/database/ - Operasi basis data :
- Koneksi dan inisialisasi basis data.
- Kueri SQL.
- Tidak ada kode UI di sini.

5. src/utils/ - Fungsi pembantu :
- Utilitas umum.
- Fungsi pembantu.
- Tidak ada kode UI di sini.

### Struktur khusus bagian UI :

src/
└── views/
    ├── main_window.py          # Main window 
    ├── components/
    │   ├── custom_widgets.py   # Reusable PyQt widgets
    │   └── dialogs.py         # Custom dialog boxes
    └── pages/
        ├── login_page.py      # Login screen
        ├── dashboard_page.py  # Main dashboard
        ├── transaction_page.py # Transaction management
        ├── budget_page.py     # Budget management
        └── saving_page.py     # Savings management

### Struktur Repository secara keseluruhan
.
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── budget.py
│   │   └── saving.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── user_controller.py
│   │   ├── transaction_controller.py
│   │   ├── budget_controller.py
│   │   └── saving_controller.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── custom_widgets.py
│   │   │   └── dialogs.py
│   │   └── pages/
│   │       ├── __init__.py
│   │       ├── login_page.py
│   │       ├── dashboard_page.py
│   │       ├── transaction_page.py
│   │       ├── budget_page.py
│   │       └── saving_page.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/
    ├── __init__.py
    ├── test_models/
    ├── test_controllers/
    └── test_views/