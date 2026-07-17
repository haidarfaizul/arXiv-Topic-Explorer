# Rencana Implementasi Web Dashboard ArXiv (Glassmorphism)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun aplikasi web dashboard interaktif satu halaman (SPA) berbasis HTML/CSS/JS murni dengan estetika Apple-style Glassmorphism di folder `03_Web_Dashboard/`.

**Architecture:** Frontend statis yang memuat data klaster secara dinamis dan melakukan inferensi klasifikasi teks secara instan di sisi klien (client-side) menggunakan algoritma pencocokan kata kunci (keyword-matching heuristic).

**Tech Stack:** HTML5, CSS3 murni (Vanilla CSS), JavaScript ES6.

## Global Constraints
- Seluruh dokumen spec/plan disimpan di folder `docs/`.
- Struktur folder harus persis sesuai spesifikasi desain.
- Tidak menggunakan framework luar (seperti React, Vue, TailwindCSS) kecuali CSS murni untuk performa pemuatan lokal instan yang bersih.

---

### Task 1: Setup & Assets Replicator
Mempersiapkan folder kerja dan menyalin berkas-berkas data yang diperlukan ke folder dashboard.

**Files:**
- Create: `03_Web_Dashboard/data/cluster_names.json`

- [ ] **Step 1: Salin berkas cluster_names.json**
Salin isi data dari `01_Clustering_and_Labelling/cluster_names.json` ke `03_Web_Dashboard/data/cluster_names.json`.
(Jika berkas pemetaan nama klaster belum ada, salin menggunakan script Python pembantu atau tulis manual di direktori tujuan).

- [ ] **Step 2: Verifikasi direktori data**
Pastikan direktori `03_Web_Dashboard/data/` terbuat dan berkas JSON terbaca dengan benar.

---

### Task 2: Pembuatan Struktur Layout (`index.html`)
Menulis dokumen HTML5 semantik dengan tata letak minimalis Apple.

**Files:**
- Create: `03_Web_Dashboard/index.html`

- [ ] **Step 1: Tulis kerangka HTML5 dasar**
Tulis tag HTML5 dasar, tautan ke Google Fonts (Inter/Outfit), stylesheet `style.css`, dan script `app.js`.

- [ ] **Step 2: Rancang navigasi (Navbar)**
Tulis header navigasi yang minimalis dengan logo proyek dan menu tab: "Overview", "Topic Explorer", "Trend Analysis", dan "Interactive Predictor".

- [ ] **Step 3: Rancang wadah konten utama (Main Containers)**
Buat kontainer dinamis untuk masing-masing tab yang akan disembunyikan/ditampilkan oleh JavaScript:
  * **Overview Container**: Widget statistik (Total Paper, Total Klaster, Metode).
  * **Topic Explorer Container**: Layout dua kolom (list klaster di kiri, detail klaster di kanan).
  * **Trend Analysis Container**: Grid 2-kolom untuk memajang 8 gambar grafik tren.
  * **Interactive Predictor Container**: Form input teks minimalis dengan tombol dan area hasil prediksi.

---

### Task 3: Pembuatan Gaya Visual (`style.css`)
Menerapkan gaya Glassmorphism premium dan layout grid responsif.

**Files:**
- Create: `03_Web_Dashboard/style.css`

- [ ] **Step 1: Definisikan CSS Variables & Resets**
Tulis variabel warna obsidian gelap, Royal Blue, Magenta, putih translusen, font-family, dan reset box-sizing standar.

- [ ] **Step 2: Buat background backlight blobs**
Terapkan dua elemen dekoratif `.glow-blob` absolut di belakang konten dengan filter blur besar untuk pendaran warna magenta dan cyan/blue.

- [ ] **Step 3: Rancang panel kaca (Glassmorphism classes)**
Tulis aturan kelas `.glass-panel` yang berisi:
  * `background: rgba(22, 22, 32, 0.55);`
  * `backdrop-filter: blur(25px) saturate(180%);`
  * `border: 1px solid rgba(255, 255, 255, 0.07);`
  * `box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);`
  * `border-radius: 16px;`

- [ ] **Step 4: Rancang interaktivitas tombol & layout responsif**
Tulis gaya hover, pergeseran opasitas border, transisi, media-queries responsif untuk tablet/seluler.

---

### Task 4: Pembuatan Logika Dashboard & Klasifikasi Mandiri (`app.js`)
Mengimplementasikan fungsi perpindahan tab, penampilan klaster, dan algoritma klasifikasi heuristik.

**Files:**
- Create: `03_Web_Dashboard/app.js`

- [ ] **Step 1: Implementasikan Tab Navigation**
Tulis event listener untuk menu tab navbar agar menyembunyikan/menampilkan kontainer tab yang sesuai secara instan dengan transisi opasitas lembut.

- [ ] **Step 2: Definisikan data kamus klaster (Cluster Dictionary)**
Di dalam JavaScript, tulis kamus data 15 klaster yang berisi: nama, kata kunci judul, kata kunci abstrak, dan daftar 3 kategori arXiv dominan (diekstrak dari profil data asli di Opsi 1). Kamus ini akan digunakan untuk menampilkan detail klaster serta untuk dasar pencocokan teks di prediktor.

- [ ] **Step 3: Implementasikan Explorer Klaster**
Rancang agar saat pengguna mengklik klaster tertentu di menu kiri, detail data klaster langsung dimuat ke panel kanan secara dinamis.

- [ ] **Step 4: Implementasikan Heuristic Classifier Engine**
Rancang fungsi klasifikasi teks:
  * Ambil teks input (Judul + Abstrak).
  * Bersihkan teks dari tanda baca dan konversi ke huruf kecil.
  * Lakukan tokenisasi sederhana (split kata).
  * Untuk setiap 15 klaster, hitung skor kecocokan berdasarkan frekuensi kemunculan kata kunci klaster (baik dari kamus judul maupun abstrak) di dalam teks masukan. Berikan bobot lebih tinggi (misal dikalikan 2.0) jika kata kunci ditemukan pada input Judul.
  * Urutkan klaster berdasarkan skor tertinggi.
  * Tampilkan 3 klaster teratas dengan bar persentase tingkat kecocokan yang dinamis dan teranimasi.
