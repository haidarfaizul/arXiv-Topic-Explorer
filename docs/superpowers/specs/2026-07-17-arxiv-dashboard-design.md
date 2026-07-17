# Spesifikasi Desain: Web Dashboard Topik ArXiv (Apple HIG-Inspired Glassmorphism)

## 1. Pendahuluan
Dokumen ini menetapkan spesifikasi desain untuk aplikasi web dashboard interaktif bertema sains data arXiv. Antarmuka dirancang mengikuti estetika **Apple Human Interface Guidelines (HIG)** yang dimodifikasi secara khusus agar orisinal, minimalis, dan elegan, menggunakan teknik **Glassmorphism murni**.

## 2. Struktur Berkas
Aplikasi web ini diletakkan pada folder `E:\Bismillah Project\Arxiv\03_Web_Dashboard\` dengan struktur:
* `index.html`: Layout HTML5 semantik dan elemen antarmuka.
* `style.css`: Aturan gaya (styling) CSS murni bertema Apple-style Glassmorphism.
* `app.js`: Logika interaktivitas tab, eksplorasi klaster, visualisasi tren, dan sistem prediksi berbasis heuristik.
* `data/cluster_names.json`: Data pemetaan klaster untuk dibaca oleh JavaScript.

## 3. Estetika Desain & Layout (HIG-Inspired Glassmorphism)
* **Warna & Latar Belakang (Deep Space Obsidian)**:
  * Warna dasar: `#0a0a0f` (obsidian gelap).
  * Efek pendaran latar belakang (*backlight*): Dua lingkaran gradien blur berwarna Royal Blue (`#3a86ff`) dan Deep Purple (`#8338ec`) dengan opasitas `0.1` di sudut-sudut strategis layar.
* **Panel & Kartu Kaca (Glass Containers)**:
  * Latar belakang: `rgba(22, 22, 30, 0.55)` (transparansi medium).
  * Pembiasan kaca: `backdrop-filter: blur(25px) saturate(180%);`
  * Perbatasan: perbatasan abu-abu tipis `1px solid rgba(255, 255, 255, 0.06)`.
  * Efek melayang: `box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);`
  * Radius sudut: `16px` (lengkungan organik khas Apple).
* **Tipografi (Typography Stack)**:
  * Menggunakan font stack sistem premium: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;`
  * Mengoptimalkan keterbacaan dengan rasio tinggi baris (*line-height*) `1.5` s.d. `1.6`.
* **Navigasi & Tabs**:
  * Bar navigasi atas yang minimalis dan tersemat (*sticky*) dengan efek buram saat halaman di-scroll (*acrylic navbar*).

## 4. Struktur Antarmuka & Fitur
Dashboard dibagi menjadi 4 tab navigasi utama:
1. **Overview**: Dashboard utama yang menampilkan statistik ringkas (Total paper 3.1M+, 15 topik klaster, two-pass pipeline) dengan grid-layout.
2. **Topic Explorer (Klaster)**: 
   * Menu list vertikal di sebelah kiri dengan indikator klaster aktif yang menyala lembut.
   * Panel sebelah kanan menampilkan deskripsi, kata kunci (Judul & Abstrak), dan profil arXiv asli.
3. **Trend Visualizer**:
   * Galeri grid berisi 8 gambar visualisasi tren tahunan dari Opsi 2.
   * Deskripsi analisis diposisikan secara bersih di bawah masing-masing gambar grafik.
4. **Interactive Predictor (Prediktor Mandiri)**:
   * Kolom input teks judul dan area teks abstrak bergaya input minimalis Apple.
   * Tombol prediksi dengan animasi pendaran halus saat hover.
   * Visualisasi tingkat kecocokan 3 klaster teratas dengan bar persentase horizontal.

## 5. Rencana Pengujian
* Menguji responsivitas pada resolusi desktop standar (1920x1080) hingga layar seluler.
* Memastikan efek blur dan saturasi visualisasi kaca berjalan optimal dan mulus tanpa lag.
