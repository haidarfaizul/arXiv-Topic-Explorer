# Spesifikasi Desain: Clustering Topik Paper ArXiv

## 1. Pendahuluan
Dokumen ini mendefinisikan rancangan notebook Jupyter untuk melakukan pengelompokan (clustering) paper ilmiah menggunakan dataset metadata ArXiv yang berukuran besar (~5.4 GB). Tujuan utamanya adalah untuk menemukan struktur topik alami dalam dataset tanpa perlu menetapkan label kategori secara manual terlebih dahulu.

## 2. Dataset & Kebutuhan Lingkungan
* **File Dataset**: [arxiv-metadata-oai-snapshot.json](file:///E:/Bismillah%20Project/Arxiv/arxiv-metadata-oai-snapshot.json) (~5.4 GB, JSON Lines format).
* **Lokasi Output Notebook**: [arxiv_topic_clustering.ipynb](file:///E:/Bismillah%20Project/Arxiv/Paper%20Topic%20Classification/arxiv_topic_clustering.ipynb).
* **Kebutuhan Library**:
  * `pandas`: Untuk manipulasi data.
  * `numpy`: Untuk operasi numerik.
  * `scikit-learn`: Untuk pemrosesan teks (`TfidfVectorizer`), pemodelan (`KMeans`), dan evaluasi.
  * `matplotlib` & `seaborn`: Untuk visualisasi data (metode Elbow, distribusi klaster).
  * `tqdm`: Untuk progress bar saat pemrosesan batch besar.

## 3. Arsitektur Sistem & Alur Kerja

```
[arxiv-metadata-oai-snapshot.json]
       | (Streaming baris-demi-baris)
       v
[Stratified Sampling (100.000 paper)]
       |
       +---> Ekstrak Title   ---> TfidfVectorizer (max: 10.000) --+
       |                                                           |--> scipy.sparse.hstack
       +---> Ekstrak Abstract ---> TfidfVectorizer (max: 25.000) --+     (Bobot Title = 2.0)
                                                                             |
                                                                             v
                                                                   [Matriks Fitur Gabungan]
                                                                             |
                                                                             v
                                                                   [KMeans Training]
                                                                             |
                                                                             v
                                                                     [Evaluasi Kata Kunci]
                                                                             |
                                                                             v
[Streaming Sisa 2,1M Paper] ---> [Transform & Predict (Batch)] ---> [Simpan CSV Hasil]
```

### 3.1 Bagian 1: Data Pipeline & Sampling
* Dataset dibaca baris-demi-baris menggunakan generator untuk menghemat RAM.
* Dilakukan **Stratified Sampling** sebanyak 100.000 paper. Stratifikasi didasarkan pada kategori utama pertama (misalnya `cs`, `math`, `hep-ph`) untuk menjamin semua domain ilmu terwakili secara proporsional.
* Kolom `title` dan `abstract` disimpan secara terpisah di memori.

### 3.2 Bagian 2: Vectorization & Clustering (Training)
* Teks dibersihkan dari *stop words* bahasa Inggris.
* **Vectorization**:
  * `TfidfVectorizer` untuk `title` dengan `max_features=10000`.
  * `TfidfVectorizer` untuk `abstract` dengan `max_features=25000`.
  * Kedua matriks digabungkan secara horizontal (`scipy.sparse.hstack`). Fitur judul dikalikan dengan bobot `2.0` agar lebih dominan dalam penentuan klaster.
* **Menentukan K**:
  * Melakukan pencarian Elbow Method pada sub-sampel kecil (10.000 paper) untuk membantu pemilihan jumlah klaster $K$.
* **Model Training & Checkpointing**:
  * Melatih model `KMeans` dari `scikit-learn` dengan parameter default $K=15$ (atau yang ditentukan pengguna) pada 100.000 sampel gabungan.
  * **Checkpoint Model**: Setelah dilatih, model `KMeans` dan kedua objek `TfidfVectorizer` akan disimpan ke disk menggunakan library `joblib` (misal: `kmeans_model.joblib`, `tfidf_title.joblib`, dan `tfidf_abstract.joblib`). Jika file-file tersebut sudah ada di disk saat notebook dijalankan kembali, notebook akan langsung memuat model yang sudah ada tanpa melakukan training ulang.
* **Analisis Centroid**:
  * Untuk setiap klaster, tampilkan 10 kata kunci teratas dari representasi judul dan abstrak untuk interpretasi topik.

### 3.3 Bagian 3: Prediksi Massal & Evaluasi
* Membaca sisa 2,1 juta paper dari file JSON secara bertahap dalam *batch* berisi 100.000 paper.
* **Inference Checkpointing**:
  * Sebelum memulai proses prediksi massal, notebook akan memeriksa apakah file hasil `arxiv_clustered_results.csv` sudah ada.
  * Jika file sudah ada, program akan menghitung jumlah baris data yang sudah diprediksi sebelumnya.
  * Saat membaca file dataset JSON, generator akan otomatis melewati (*skip*) sejumlah data yang sudah selesai diproses tersebut. Hasil baru akan di-append (ditambahkan ke akhir file) tanpa menulis ulang dari awal.
* Setiap batch ditransformasikan menggunakan TF-IDF yang sudah terlatih, diprediksi klasternya menggunakan model KMeans, dan hasilnya langsung ditulis secara bertahap (*append*) ke file CSV output `arxiv_clustered_results.csv`.
* Menampilkan visualisasi distribusi paper di setiap klaster hasil prediksi.
* Melakukan evaluasi silang dengan membandingkan kategori arXiv asli yang paling dominan di setiap klaster hasil prediksi guna memvalidasi relevansi topik.

## 4. Rencana Pengujian & Keamanan
* **Keamanan Memori**: Memastikan kode notebook menggunakan generator dan pemrosesan batch agar tidak melebihi batas memori sistem (RAM).
* **Penanganan File Kosong/Kotor**: Menghindari crash jika ada abstrak atau judul yang kosong dengan imputasi teks kosong (`""`).
* **Mekanisme Resume**: Menguji apakah sistem checkpoint dapat mendeteksi file parsial dan melanjutkan proses dari titik terakhir dengan benar.
* **Verifikasi Akhir**: Memastikan notebook dapat dijalankan dari atas sampai bawah (Restart & Run All) tanpa error.
