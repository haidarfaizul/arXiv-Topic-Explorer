# arXiv Topic Explorer & Clustering Dashboard

Proyek sains data terpadu untuk melakukan pengelompokan (*clustering*) topik, analisis tren temporal (tahunan) dari tahun 1993 hingga 2026, serta penyajian antarmuka dashboard interaktif menggunakan **3,1 juta+** metadata paper ilmiah dari arXiv.

## 📊 Dataset Utama
Dataset yang digunakan dalam proyek ini adalah metadata publikasi ilmiah arXiv resmi yang dapat diunduh di:
* **Tautan Dataset (Kaggle)**: [Kaggle Cornell University arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)
* **Format & Ukuran**: File berkas JSON Lines (~5.4 GB) bernama `arxiv-metadata-oai-snapshot.json`. Letakkan berkas ini di root direktori proyek Anda setelah diunduh.

---

## 📂 Struktur Direktori Proyek

Proyek ini dipisahkan menjadi beberapa folder berdasarkan tahapan analisis untuk mempermudah dokumentasi:

```text
Arxiv/ (Root)
│
├── arxiv-metadata-oai-snapshot.json  <-- File Dataset Utama (Unduh dari Kaggle, taruh di sini)
├── README.md                         <-- Berkas Panduan Utama (Berkas ini)
│
├── 01_Clustering_and_Labelling/
│   ├── arxiv_topic_clustering.ipynb   <-- Notebook latih model & batch prediction 2.2M paper
│   ├── checkpoints/                  <-- Model KMeans & TF-IDF (.joblib) hasil training
│   ├── arxiv_clustered_results.csv   <-- Hasil prediksi klaster seluruh paper (CSV)
│   └── cluster_names.json             <-- Pemetaan 15 Klaster ke nama topik akademis resmi
│
├── 02_Trend_Analysis/
│   ├── topic_trend_analysis.ipynb     <-- Notebook analisis tren popularitas temporal
│   └── plots/                        <-- 8 Visualisasi grafik tren tahunan (PNG)
│
└── 03_Web_Dashboard/
    ├── index.html                    <-- Aplikasi web dashboard (Apple-style Glassmorphism)
    ├── style.css                     <-- Desain visual dashboard (CSS murni)
    ├── app.js                        <-- Logika interaktif & Mesin Prediktor (JS murni)
    └── data/
        └── cluster_names.json        <-- Salinan pemetaan klaster untuk aplikasi web
```

---

## ⚙️ Persyaratan Sistem & Dependensi

Proyek ini dibangun menggunakan Python 3.10+ dengan library sains data berikut:
* `pandas`
* `numpy`
* `scipy`
* `scikit-learn`
* `joblib`
* `matplotlib`
* `seaborn`
* `jupyter`

Anda dapat menginstal dependensi di atas menggunakan pip:
```bash
pip install pandas numpy scipy scikit-learn joblib matplotlib seaborn jupyter
```

---

## 🚀 Alur Kerja & Cara Menjalankan

### Langkah 1: Pelatihan Model & Prediksi Klaster
1. Letakkan berkas `arxiv-metadata-oai-snapshot.json` di root folder proyek.
2. Jalankan notebook [01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb](file:///E:/Bismillah%20Project/Arxiv/01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb).
3. Notebook ini akan mengambil 100.000 paper sampel terstratifikasi secara hemat RAM untuk melatih model TF-IDF dan K-Means ($K=15$).
4. Model akan disimpan otomatis di folder `checkpoints/`.
5. Notebook akan melakukan prediksi (*inference*) secara berkelompok (*batch*) pada sisa 2,1 juta paper dan menyimpannya secara progresif ke berkas `arxiv_clustered_results.csv`. (Proses ini mendukung melanjutkan otomatis jika terhenti).

### Langkah 2: Analisis Tren Temporal
1. Jalankan notebook [02_Trend_Analysis/topic_trend_analysis.ipynb](file:///E:/Bismillah%20Project/Arxiv/02_Trend_Analysis/topic_trend_analysis.ipynb).
2. Notebook ini akan mem-parsing tahun publikasi langsung dari ID paper dan mengagregasi popularitas relatif setiap klaster per tahun (1993 - 2026).
3. Menghasilkan dan menyimpan **8 grafik analisis tren ilmiah** ke dalam folder `02_Trend_Analysis/plots/` secara otomatis.

### Langkah 3: Menjalankan Web Dashboard
1. Buka folder `03_Web_Dashboard/`.
2. Klik ganda pada berkas [03_Web_Dashboard/index.html](file:///E:/Bismillah%20Project/Arxiv/03_Web_Dashboard/index.html) untuk langsung membukanya di browser Anda (Chrome, Firefox, Safari, atau Edge).
3. **Fitur Dashboard**:
   * **Overview**: Tampilan statistik ringkas proyek secara elegan.
   * **Topic Explorer**: Jelajahi detail kata kunci dan kategori asli dari masing-masing 15 klaster topik.
   * **Trend Analysis**: Lihat 8 visualisasi evolusi topik sains dari tahun 1993 hingga 2026 yang sudah diproduksi.
   * **Interactive Predictor**: Masukkan judul dan abstrak paper baru Anda untuk mendapatkan prediksi klasifikasinya secara *real-time* langsung di browser (client-side execution).

---

## 🎨 Desain Visual Dashboard
Dashboard web dirancang mengikuti estetika **Apple HIG (Human Interface Guidelines)** yang bersih dengan efek **Glassmorphism murni**:
* **Obsidian Base**: Tema warna gelap pekat dengan pendaran gradien redup (*glow blobs*) biru dan ungu.
* **Translucent Materials**: Panel kaca menggunakan properti `backdrop-filter: blur(25px) saturate(180%);` dengan perbatasan tipis transparan.
* **Responsive Layout**: Antarmuka adaptif untuk layar desktop maupun perangkat seluler.
