# Spesifikasi Desain: Web Dashboard Topik ArXiv (Glassmorphism)

## 1. Pendahuluan
Dokumen ini menetapkan spesifikasi desain untuk aplikasi web satu halaman (Single Page Application) dashboard interaktif yang menyajikan hasil pengelompokan topik paper arXiv, visualisasi tren temporal, dan alat klasifikasi interaktif menggunakan gaya visual **Glassmorphism**.

## 2. Kebutuhan Struktur Berkas
Aplikasi web ini diletakkan pada folder `E:\Bismillah Project\Arxiv\03_Web_Dashboard\` dengan struktur:
* `index.html`: Struktur HTML5 semantik dan elemen layout.
* `style.css`: Aturan gaya (styling) Glassmorphism premium (CSS murni).
* `app.js`: Logika aplikasi, pengelolaan tab, pemuatan visualisasi, dan mesin prediksi mandiri.
* `data/cluster_names.json`: Salinan data pemetaan klaster yang akan dibaca oleh JavaScript.

## 3. Gaya Visual & Estetika (Glassmorphism)
* **Background**:
  * Warna dasar: `#09090e` (hampir hitam).
  * Dua lingkaran gradien besar (*glow blobs*) dengan posisi absolut di belakang panel:
    * Blob 1 (Cyan/Blue): `#00f2fe` di sudut kiri atas, blur `150px`, opacity `0.15`.
    * Blob 2 (Magenta/Purple): `#4facfe` atau ungu di sudut kanan bawah, blur `150px`, opacity `0.15`.
* **Panel Kaca (Glass Panels)**:
  * `background: rgba(18, 18, 28, 0.65);`
  * `backdrop-filter: blur(20px);`
  * `border: 1px solid rgba(255, 255, 255, 0.08);`
  * `box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);`
  * `border-radius: 16px;`
* **Typography**:
  * Font: Google Fonts 'Outfit' dan 'Inter'.
  * Skema warna teks: Putih terang untuk judul, abu-abu muda (`#a0aec0`) untuk deskripsi, dan cyan neon (`#00f2fe`) untuk sorotan/indikator aktif.

## 4. Antarmuka Pengguna & Fitur
Dashboard dibagi menjadi 4 tab navigasi utama:
1. **Overview**: Menyajikan metrik proyek ringkas (Total 3.1M paper dianalisis, 15 Klaster Akademis, Two-stage Clustering).
2. **Topic Explorer (Klaster)**: 
   * Panel navigasi sisi kiri yang interaktif berisi daftar 15 klaster.
   * Panel sisi kanan yang menampilkan nama klaster, kata kunci teratas (Title/Abstract), serta komposisi kategori arXiv asli yang dominan.
3. **Trend Visualizer**:
   * Galeri berisi 8 grafik tren temporal yang diekspor dari Opsi 2.
   * Penjelasan interpretasi ilmiah di samping/bawah setiap grafik.
4. **Interactive Predictor (Prediktor Mandiri)**:
   * Form masukan teks untuk Judul dan Abstrak paper baru.
   * Tombol klasifikasi yang menjalankan mesin pencocokan kata kunci (keyword-matching/score heuristic) berdasarkan 10 kata kunci teratas per klaster.
   * Menampilkan visualisasi persentase tingkat kecocokan untuk 3 klaster teratas dengan bar animasi yang cantik.

## 5. Rencana Pengujian
* Memastikan efek `backdrop-filter` berfungsi dengan baik di peramban modern (Chrome, Edge, Firefox, Safari).
* Memastikan tata letak bersifat responsif pada berbagai ukuran layar.
* Memastikan alat klasifikasi interaktif bekerja secara offline tanpa broken imports.
