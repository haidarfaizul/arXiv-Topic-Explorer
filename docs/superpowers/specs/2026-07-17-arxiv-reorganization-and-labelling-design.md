# Spesifikasi Desain: Reorganisasi Proyek & Analisis Penamaan Klaster ArXiv

## 1. Pendahuluan
Dokumen ini menetapkan struktur folder proyek yang rapi dan terorganisir untuk memisahkan setiap tahap pemrosesan data, visualisasi tren, dan dashboard web. Dokumen ini juga merancang langkah-langkah untuk Opsi 1 (Analisis & Penamaan Klaster) setelah file notebook dipindahkan.

## 2. Struktur Folder Proyek
Semua file proyek akan direorganisasi ke dalam struktur berikut:
* `E:\Bismillah Project\Arxiv\arxiv-metadata-oai-snapshot.json` (Dataset utama tetap di root)
* `E:\Bismillah Project\Arxiv\01_Clustering_and_Labelling\`
  * `arxiv_topic_clustering.ipynb` (Notebook dipindah dari folder "Paper Topic Classification")
  * `checkpoints/` (Folder model `joblib` dipindah dari folder "Paper Topic Classification")
  * `arxiv_clustered_results.csv` (Hasil prediksi CSV dipindah dari root/folder sebelumnya)
* `E:\Bismillah Project\Arxiv\02_Trend_Analysis\`
  * `plots/` (Untuk menyimpan visualisasi tren temporal)
* `E:\Bismillah Project\Arxiv\03_Web_Dashboard\`
  * `index.html`
  * `style.css`
  * `app.js`
  * `data/`

## 3. Alur Kerja Reorganisasi & Opsi 1
1. **Reorganisasi Berkas**:
   * Membuat folder `01_Clustering_and_Labelling/`, `02_Trend_Analysis/plots/`, dan `03_Web_Dashboard/data/`.
   * Memindahkan file `Paper Topic Classification/arxiv_topic_clustering.ipynb` ke `01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb`.
   * Memindahkan folder model checkpoints (jika ada) ke `01_Clustering_and_Labelling/checkpoints/`.
   * Menghapus folder kosong `Paper Topic Classification/`.
2. **Analisis Klaster & Penamaan (Opsi 1)**:
   * Mengumpulkan kata kunci teratas (Top 10 Title/Abstract Words) dan kategori arXiv asli terpopuler dari setiap klaster yang telah dihasilkan oleh pengguna.
   * Membuat file pemetaan JSON `01_Clustering_and_Labelling/cluster_names.json` yang memetakan nomor klaster (0-14) ke nama label topik akademis yang representatif (misal: "Deep Learning & NLP", "Quantum Mechanics").

## 4. Pengujian & Verifikasi
* Verifikasi bahwa Jupyter Notebook di lokasi baru tetap dapat diakses dan tidak mengalami broken links (path dataset disesuaikan menjadi `../arxiv-metadata-oai-snapshot.json`).
* Verifikasi bahwa folder `Paper Topic Classification` telah terhapus sepenuhnya.
