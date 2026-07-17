# arXiv Topic Explorer & Clustering Dashboard

Menyajikan analisis pengelompokan (*clustering*) topik akademis, evolusi tren sains dari tahun 1993 hingga 2026, dan dashboard visualisasi interaktif menggunakan **3,1 juta+** metadata paper ilmiah dari arXiv.

Proyek ini menggunakan model pembelajaran mesin K-Means tak terarah yang dilatih pada 100.000 sampel representatif (stratified reservoir sampling) dan dieksekusi secara bertahap (*batch inference*) untuk menghemat memori RAM.

---

## 🚀 Fitur Utama
* **Two-Pass Stratified Reservoir Sampling**: Pipeline data hemat RAM $O(1)$ untuk membaca data berukuran 5.4 GB secara bertahap tanpa Out-of-Memory (OOM).
* **Weighted TF-IDF Vectorization**: Memberikan pembobotan ganda (2.0) pada judul dibandingkan abstrak untuk meningkatkan akurasi representasi klaster.
* **Batch Inference & Resume Checkpoint**: Dapat memprediksi 2.1 juta paper sisa dalam ukuran batch 100k, lengkap dengan pemulihan otomatis (*resume*) jika proses terhenti di tengah jalan.
* **Apple HIG-Inspired Web Dashboard**: Antarmuka web satu halaman (SPA) berbasis **Glassmorphism murni** (HTML/CSS/JS statis) dengan alat klasifikasi teks interaktif secara *real-time* langsung di sisi klien (*client-side*).

---

## 📊 Dataset Utama
Dataset proyek ini diambil langsung dari repositori arXiv resmi di Kaggle:
* **Tautan Unduhan**: [Kaggle Cornell University arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)
* **Penyimpanan**: Unduh file `arxiv-metadata-oai-snapshot.json` (~5.4 GB) dan letakkan langsung di direktori utama (root) repositori ini.

---

## 📂 Struktur Direktori Proyek

```text
Arxiv/ (Root)
│
├── arxiv-metadata-oai-snapshot.json  <-- File Dataset (Letakkan di sini setelah diunduh)
├── README.md                         <-- Berkas Panduan Repositori (Berkas ini)
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

## ⚙️ Persyaratan Sistem & Instalasi

Proyek ini dibangun menggunakan Python 3.10+ dengan library sains data berikut:
* `pandas`
* `numpy`
* `scipy`
* `scikit-learn`
* `joblib`
* `matplotlib`
* `seaborn`
* `jupyter`

1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/USERNAME/Arxiv-Topic-Explorer.git
   cd Arxiv-Topic-Explorer
   ```

2. **Instal dependensi**:
   ```bash
   pip install pandas numpy scipy scikit-learn joblib matplotlib seaborn jupyter
   ```

3. **Unduh Dataset**: Unduh berkas metadata dari Kaggle dan taruh di root direktori dengan nama `arxiv-metadata-oai-snapshot.json`.

---

## 🚀 Alur Kerja Eksekusi

### Langkah 1: Pelatihan Model & Prediksi Klaster
Jalankan Jupyter Notebook di [01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb](./01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb).
* Sel pertama akan memvalidasi data pipeline.
* Model KMeans ($K=15$) akan dilatih dan disimpan di folder `checkpoints/`.
* Proses batch inference sisa paper akan berjalan dan memproduksi berkas `arxiv_clustered_results.csv`.

### Langkah 2: Analisis Tren Temporal
Jalankan Jupyter Notebook di [02_Trend_Analysis/topic_trend_analysis.ipynb](./02_Trend_Analysis/topic_trend_analysis.ipynb).
* Mengekstrak tahun terbit dari kolom ID untuk analisis tren tahunan (1993 - 2026).
* Menghasilkan **8 grafik visualisasi** tren di folder [02_Trend_Analysis/plots/](./02_Trend_Analysis/plots/).

### Langkah 3: Menjalankan Web Dashboard
1. Buka folder [03_Web_Dashboard/](./03_Web_Dashboard/).
2. Klik ganda pada berkas [index.html](./03_Web_Dashboard/index.html) untuk langsung membukanya di browser Anda secara offline.
3. Anda dapat menjelajahi statistik (Overview), rincian topik klaster (Topic Explorer), visualisasi grafik (Trend Analysis), serta menguji draf paper Anda secara langsung pada tab **Interactive Predictor**.

---

## 🎨 Desain Visual Dashboard
Dashboard web dirancang mengikuti estetika **Apple HIG (Human Interface Guidelines)** yang bersih dengan efek **Glassmorphism murni**:
* **Obsidian Base**: Tema warna gelap obsidian (`#07070a`) dengan pendaran gradien biru dan ungu redup di latar belakang.
* **Translucent Materials**: Panel kaca menggunakan filter pembiasan cahaya `backdrop-filter: blur(25px) saturate(190%);` dengan perbatasan tipis transparan.
* **Responsive Layout**: Antarmuka adaptif untuk layar desktop maupun perangkat seluler.

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah **MIT License**. Lihat berkas `LICENSE` untuk rincian selengkapnya.
