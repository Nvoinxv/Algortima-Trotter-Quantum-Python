# Simulasi Trotter Algoritma Kuantum Komputer

## Introduction
Halo! Di sini gw mau buat simulasi Trotter Algoritma Kuantum Komputer. Gw ambil dari paper [di sini](https://arxiv.org/pdf/2508.15691), jadi kalau kalian mau baca, silakan cek di situ.  

Inti dari paper tersebut adalah:  

- Untuk memecahkan **PDE** (Partial Differential Equation), kita menggunakan metode Trotter.  
- PDE biasa digunakan untuk simulasi **aliran udara, fluida**, dan lain-lain, yang perhitungannya sering **acak** atau **non-linear**, sehingga komputer klasik sulit menghitung lebih cepat.  
- Algoritma ini menggunakan komponen **standarisasi, generalisasi, dan evolusi**. Bagian **evolusi** yang paling berat.  
- Karena laptop gw masih klasik, proyek ini bakal lambat dan menggunakan **grid 2x2**.  
  - Kalau pakai **3x3 atau lebih**, waktu komputasi bisa sangat lama.  
- Saran gw: pakai library **Quantum Python**, tapi karena gw buat setengah dari scratch, tetap pakai library basic, jadi lebih lambat.  

## Cara Menjalankan Projek

- Untuk menjalankan per-folder:

```bash
python -m TrotterAlgorithm.[nama_folder].[nama_proyek]
python -m TrotterAlgorithm.main
```

Kalau kamu mau, aku bisa buatkan versi **lebih “GitHub-friendly” lagi** dengan:  

- Badge (misal Python version, License)  
- Struktur list rapi untuk fitur proyek  
- Contoh output atau screenshot supaya lebih menarik  

Mau aku buatkan versi itu juga?

