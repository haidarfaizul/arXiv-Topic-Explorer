# ArXiv Topic Clustering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun Jupyter Notebook interaktif (`arxiv_topic_clustering.ipynb`) untuk clustering 2.2M paper ArXiv dengan model yang dilatih pada 100k sampel, lengkap dengan fitur resume checkpoint jika terhenti di tengah jalan. Semua kode ditulis langsung di dalam notebook.

**Architecture:** Semua fungsi utilitas, logika pemodelan, evaluasi, dan unit test (berbasis assertion cell) ditulis langsung di dalam sel Jupyter Notebook.

**Tech Stack:** Python, Jupyter Notebook, scikit-learn, pandas, numpy, joblib, matplotlib, seaborn, tqdm.

## Global Constraints
- Meminimalkan RAM dengan menggunakan Python generator untuk membaca JSON lines secara bertahap.
- Model TF-IDF dan KMeans harus disimpan menggunakan `joblib` agar tidak perlu dilatih ulang jika notebook dijalankan ulang.
- Batch inference pada 2,1M paper sisa harus mendukung resume dengan mendeteksi baris yang sudah tertulis di CSV keluaran.
- Semua kode harus bebas dari TBD atau TODO.
- Seluruh pengujian dijalankan langsung di dalam notebook dengan menjalankan sel pengujian berisi `assert`.

---

### Task 1: Setup & Data Pipeline in Notebook
Membuat kerangka notebook Jupyter awal, mengimplementasikan generator data dan sampling stratifikasi dalam sel notebook, serta membuat sel pengujian untuk memverifikasi fungsionalitasnya.

**Files:**
- Create: `Paper Topic Classification/arxiv_topic_clustering.ipynb`

**Interfaces:**
- Cell 1: Import libraries
- Cell 2: `stream_arxiv_metadata(filepath: str)` -> Generator yielding dict
- Cell 3: `get_stratified_sample(filepath: str, sample_size: int = 100000)` -> tuple (list of titles, list of abstracts, list of categories)
- Cell 4: Unit test cell containing test functions with assertions.

- [ ] **Step 1: Tulis kerangka notebook beserta tes gagal**
Buat file Jupyter Notebook `Paper Topic Classification/arxiv_topic_clustering.ipynb` dengan struktur JSON notebook dasar yang mendefinisikan sel-sel awal dan sel pengujian yang memanggil `stream_arxiv_metadata` dan `get_stratified_sample`.
(Karena notebook baru dibuat, sel pengujian akan gagal atau error saat dieksekusi).

- [ ] **Step 2: Jalankan notebook untuk memverifikasi kegagalan**
Run: `jupyter nbconvert --to notebook --execute "Paper Topic Classification/arxiv_topic_clustering.ipynb"`
Expected: FAIL dengan NameError karena fungsi streaming/sampling belum diimplementasikan.

- [ ] **Step 3: Tulis implementasi lengkap untuk Task 1 di dalam sel notebook**
Isi sel notebook dengan implementasi lengkap menggunakan generator dan reservoir sampling dua langkah:
[Detail implementasi diabaikan karena sudah selesai]

- [ ] **Step 4: Jalankan notebook untuk memverifikasi kelulusan**
Run: `jupyter nbconvert --to notebook --execute "Paper Topic Classification/arxiv_topic_clustering.ipynb"`
Expected: PASS (Semua sel tereksekusi tanpa error).

- [ ] **Step 5: Commit**
Run:
```bash
git add "Paper Topic Classification/arxiv_topic_clustering.ipynb"
git commit -m "feat: init notebook with data pipeline and unit tests"
```

---

### Task 2: Vectorization & Clustering (Training)
Menambahkan logika ekstraksi fitur TF-IDF terpisah, penggabungan bobot title, pelatihan KMeans, dan penyimpanan checkpoint model menggunakan `joblib`.

**Files:**
- Modify: `Paper Topic Classification/arxiv_topic_clustering.ipynb`

**Interfaces:**
- Cell 5: `fit_and_save_models(titles, abstracts, k, output_dir)` -> tuple (kmeans, tfidf_title, tfidf_abstract)
- Cell 6: `load_models(output_dir)` -> tuple (kmeans, tfidf_title, tfidf_abstract) atau None
- Cell 7: Unit test cell verifying model fit, save, and load.

[Langkah detail diabaikan]

---

### Task 3: Batch Inference & Resuming Checkpoint
Menambahkan logika prediksi massal bertahap ke dalam notebook, lengkap dengan deteksi file keluaran CSV untuk melanjutkan (resume) otomatis dari titik terakhir.

**Files:**
- Modify: `Paper Topic Classification/arxiv_topic_clustering.ipynb`

[Langkah detail diabaikan]

---

### Task 4: Visualization, Centroids & Execution Run
Menambahkan visualisasi Elbow Method, analisis kata kunci centroid, presentasi grafik, dan sel eksekusi utama yang siap dijalankan oleh pengguna.

**Files:**
- Modify: `Paper Topic Classification/arxiv_topic_clustering.ipynb`

[Langkah detail diabaikan]
