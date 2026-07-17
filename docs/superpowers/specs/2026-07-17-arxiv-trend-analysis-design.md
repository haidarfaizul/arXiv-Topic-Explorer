# Spesifikasi Desain: Analisis Tren Topik ArXiv dari Waktu ke Waktu

## 1. Pendahuluan
Dokumen ini mendefinisikan rancangan notebook Jupyter `02_Trend_Analysis/topic_trend_analysis.ipynb` untuk menganalisis dan memvisualisasikan tren temporal (tahunan) dari 15 klaster/topik paper ilmiah yang telah diidentifikasi di arXiv dari tahun 1993 hingga 2026.

## 2. Input Data
* **Lokasi File Prediksi**: `E:\Bismillah Project\Arxiv\01_Clustering_and_Labelling\arxiv_clustered_results.csv` (berisi kolom `id`, `cluster`, `title`, `abstract`, `categories`).
* **Lokasi File Pemetaan Nama**: `E:\Bismillah Project\Arxiv\01_Clustering_and_Labelling\cluster_names.json`.
* **Lokasi Output Notebook**: `E:\Bismillah Project\Arxiv\02_Trend_Analysis\topic_trend_analysis.ipynb`.
* **Lokasi Penyimpanan Grafik**: `E:\Bismillah Project\Arxiv\02_Trend_Analysis\plots/`.

## 3. Ekstraksi Tahun Publikasi
Tahun publikasi akan diekstraksi langsung dari kolom `id` di CSV untuk efisiensi RAM:
* ID Numerik (post-2007, e.g. `YYMM.NNNN`):
  * Tahun terbit = `2000 + YY`.
* ID Lama (pre-2007, e.g. `kategori/YYMMNNN`):
  * Jika `YY >= 93`, Tahun terbit = `1900 + YY`.
  * Jika `YY < 93` (e.g. `00` hingga `07`), Tahun terbit = `2000 + YY`.

## 4. Visualisasi Tren (Total 8 Grafik)
Notebook akan menghasilkan dan menyimpan grafik-grafik berikut ke dalam `02_Trend_Analysis/plots/`:
1. **Trend Line Plot**: Persentase popularitas relatif klaster dari tahun ke tahun.
2. **Heatmap Tren Temporal**: Peta panas 2D (Tahun vs Klaster) berdasarkan persentase relatif popularitas.
3. **Stacked Area Chart**: Komposisi keseluruhan 15 klaster dari waktu ke waktu.
4. **Topic Growth Velocity (Bar Chart)**: Top 5 topik dengan laju pertumbuhan persentase tertinggi dalam 5 tahun terakhir.
5. **Topic Decline Velocity (Bar Chart)**: Top 5 topik dengan laju penurunan persentase terbesar dalam 5 tahun terakhir.
6. **Dominant Topic Timeline**: Visualisasi linimasa topik terpopuler (#1) per tahun.
7. **Cluster Year Distribution (Box/Violin Plot)**: Distribusi tahun terbit paper untuk setiap klaster untuk mendeteksi bidang matang vs berkembang.
8. **Cumulative Growth Line Plot**: Akumulasi total jumlah paper per klaster dari tahun ke tahun.

## 5. Rencana Pengujian
* Menguji parser ID pada sampel berbagai format ID arXiv (lama & baru) untuk memastikan akurasi tahun.
* Menguji kelancaran kalkulasi persetase dan kecepatan pertumbuhan tanpa error pembagian dengan nol.
* Memastikan semua grafik tersimpan ke folder `plots/` dalam format PNG resolusi tinggi.
