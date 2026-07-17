# Rencana Implementasi Analisis Tren Topik ArXiv

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun Jupyter Notebook (`02_Trend_Analysis/topic_trend_analysis.ipynb`) untuk menganalisis pergeseran minat akademis tahunan dan menghasilkan 8 visualisasi tren yang disimpan ke folder `02_Trend_Analysis/plots/`.

**Architecture:** Membaca berkas hasil prediksi CSV secara bertahap atau sekaligus (tergantung ukuran), memproses tahun rilis via fungsi parsing ID kustom, menghitung persentase popularitas relatif, serta melukis grafik menggunakan Matplotlib dan Seaborn.

**Tech Stack:** Python, Jupyter Notebook, Pandas, NumPy, Matplotlib, Seaborn.

## Global Constraints
- Seluruh dokumen spec/plan disimpan di folder `docs/`.
- Struktur folder harus persis sesuai spesifikasi desain.
- Tidak boleh membuat file `.py` eksternal.

---

### Task 1: Setup & ID Parser Unit Test
Membuat notebook baru, menulis fungsi parser ID arXiv ke tahun terbit, dan memverifikasinya menggunakan unit test assertion di dalam notebook.

**Files:**
- Create: `02_Trend_Analysis/topic_trend_analysis.ipynb`

**Interfaces:**
- Cell 1: Import library (`pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`, `json`, `os`).
- Cell 2: `extract_year_from_id(arxiv_id)` -> `int` (atau `None` jika tidak valid).
- Cell 3: Unit test cell berisi test assertions.

- [ ] **Step 1: Buat notebook awal**
Buat file notebook di `02_Trend_Analysis/topic_trend_analysis.ipynb` dengan sel impor dan kerangka fungsi `extract_year_from_id`.

- [ ] **Step 2: Implementasikan fungsi parser tahun**
Tulis algoritma parser tahun berdasarkan aturan:
  * Bersihkan string `arxiv_id` dari spasi.
  * Jika terdapat karakter `/` (format lama):
    * Ambil bagian setelah `/`. Ambil 2 karakter pertama sebagai `YY`.
    * Jika `YY` >= 93, tahun = `1900 + YY`. Jika `YY` < 93, tahun = `2000 + YY`.
  * Jika tidak ada `/`:
    * Hapus titik (`.`) jika ada. Ambil 2 digit pertama sebagai `YY`.
    * Jika `YY` berupa angka valid:
      * Jika `YY` >= 93, tahun = `1900 + YY`. Jika `YY` < 93, tahun = `2000 + YY`.
  * Kembalikan tahun sebagai integer.

- [ ] **Step 3: Buat unit test assertion**
Buat sel unit test yang memvalidasi hasil ekstraksi untuk berbagai kasus:
  * `0704.0001` -> `2007`
  * `hep-ph/0302123` -> `2003`
  * `9301123` -> `1993`
  * `math/9903120` -> `1999`
  * `2101.12345` -> `2021`
Jalankan sel pengujian ini untuk memastikan parser 100% akurat.

---

### Task 2: Data Aggregation & Velocity Metrics
Memuat file CSV hasil prediksi dan memproses data statistik agregasi tahunan.

**Files:**
- Modify: `02_Trend_Analysis/topic_trend_analysis.ipynb`

**Interfaces:**
- Cell 4: Membaca file `arxiv_clustered_results.csv` ke DataFrame Pandas, menerapkan fungsi `extract_year_from_id`, dan memuat pemetaan nama klaster dari `cluster_names.json`.
- Cell 5: Menghitung persentase popularitas relatif klaster per tahun.
- Cell 6: Menghitung metrik kecepatan pertumbuhan/penurunan (Growth & Decline Velocity) dalam 5 tahun terakhir (2021-2026).

- [ ] **Step 1: Muat data & terapkan parser**
Muat `arxiv_clustered_results.csv`. Terapkan `extract_year_from_id` ke kolom `id` untuk membuat kolom baru `year`. Filter baris yang tahunnya tidak valid atau di luar jangkauan 1993-2026.

- [ ] **Step 2: Agregasikan data**
Hitung jumlah paper per `(year, cluster)`. Hitung total paper per `year`. Bagi jumlah paper per klaster dengan total paper di tahun bersangkutan untuk mendapatkan proporsi popularitas relatif (persentase).

- [ ] **Step 3: Hitung laju kecepatan (Velocity)**
Hitung selisih persentase relatif antara tahun akhir (misalnya 2026 atau 2025) dengan 5 tahun sebelumnya (misalnya 2021 atau 2020) untuk menemukan topik yang tumbuh paling cepat (Growth Velocity) dan yang menurun paling tajam (Decline Velocity).

---

### Task 3: Visualisasi & Ekspor Grafik
Membuat sel plotting untuk masing-masing dari 8 visualisasi tren dan menyimpannya ke folder `plots/`.

**Files:**
- Modify: `02_Trend_Analysis/topic_trend_analysis.ipynb`
- Create: File PNG grafik di `02_Trend_Analysis/plots/`

- [ ] **Step 1: Plot grafik 1 s.d. 3 (Tren Utama)**
  * **Grafik 1: Line Plot Tren Relatif** (menampilkan pergerakan persentase semua klaster dari tahun ke tahun).
  * **Grafik 2: Heatmap Tren Temporal** (Peta panas Tahun vs Klaster).
  * **Grafik 3: Stacked Area Chart** (Komposisi area bertumpuk dari 15 klaster).

- [ ] **Step 2: Plot grafik 4 s.d. 5 (Velocity)**
  * **Grafik 4: Top 5 Hottest Topics (Growth Velocity)**.
  * **Grafik 5: Top 5 Coolest Topics (Decline Velocity)**.

- [ ] **Step 3: Plot grafik 6 s.d. 8 (Profil & Akumulasi)**
  * **Grafik 6: Dominant Topic Timeline** (Menampilkan label topik nomor 1 per tahun).
  * **Grafik 7: Cluster Year Distribution (Box Plot)** (Menampilkan usia sebaran terbitan per klaster).
  * **Grafik 8: Cumulative Growth Line Plot** (Akumulasi total paper per klaster).

- [ ] **Step 4: Simpan berkas**
Pastikan semua grafik secara otomatis disimpan ke `plots/` saat sel dijalankan menggunakan `plt.savefig()`.
