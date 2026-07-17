# Reorganisasi & Penamaan Klaster ArXiv Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Menata ulang struktur folder proyek agar rapi dan memetakan nomor klaster hasil prediksi ke nama topik akademis yang representatif dengan menganalisis hasil eksekusi notebook.

**Architecture:** Memindahkan berkas-berkas secara aman via sistem berkas, memprogram parser Python untuk membaca output notebook, dan menyimpan pemetaan nama klaster ke file `cluster_names.json`.

**Tech Stack:** Python, Git, JSON.

## Global Constraints
- Seluruh dokumen dan metadata spec/plan disimpan di folder `docs/`.
- Struktur folder harus persis sesuai spesifikasi desain.
- Tidak boleh membuat file `.py` yang tidak perlu (YAGNI).

---

### Task 1: Reorganisasi Direktori
Membuat folder baru dan memindahkan berkas-berkas clustering ke folder `01_Clustering_and_Labelling/`.

**Files:**
- Modify: Memindahkan `Paper Topic Classification/arxiv_topic_clustering.ipynb` -> `01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb`
- Delete: `Paper Topic Classification/` (jika sudah kosong)

- [ ] **Step 1: Buat direktori baru**
Buat folder-folder berikut jika belum ada:
  * `01_Clustering_and_Labelling/`
  * `02_Trend_Analysis/plots/`
  * `03_Web_Dashboard/data/`

- [ ] **Step 2: Pindahkan file clustering**
Pindahkan berkas notebook dari `Paper Topic Classification/arxiv_topic_clustering.ipynb` ke `01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb`.
Jika ada folder `checkpoints/` di `Paper Topic Classification/checkpoints/` atau root, pindahkan ke `01_Clustering_and_Labelling/checkpoints/`.
Jika ada file `arxiv_clustered_results.csv` di root, pindahkan ke `01_Clustering_and_Labelling/arxiv_clustered_results.csv`.

- [ ] **Step 3: Sesuaikan path di dalam notebook**
Buka notebook di `01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb` and pastikan path dataset `DATASET_PATH` merujuk ke `../arxiv-metadata-oai-snapshot.json` karena notebook sekarang berada di dalam subfolder.

- [ ] **Step 4: Bersihkan direktori lama**
Hapus direktori kosong `Paper Topic Classification/`.

- [ ] **Step 5: Verifikasi pemindahan**
Jalankan verifikasi untuk memastikan seluruh berkas berada di tempat yang baru dan folder lama telah terhapus.
Commit hasil reorganisasi ke Git.

---

### Task 2: Analisis Hasil & Penamaan Klaster (Labelling)
Membaca output sel centroid dan profiling kategori dari file notebook yang sudah dijalankan untuk memetakan klaster ke topik akademis resmi.

**Files:**
- Create: `01_Clustering_and_Labelling/cluster_names.json`

- [ ] **Step 1: Tulis script parser output notebook**
Buat script python sementara `read_outputs.py` untuk mengekstrak dan menampilkan output teks dari sel visualisasi centroid dan profiling kategori arXiv dalam file `01_Clustering_and_Labelling/arxiv_topic_clustering.ipynb`.

- [ ] **Step 2: Analisis kata kunci & kategori**
Analisis kata kunci dan kategori dominan untuk setiap dari 15 klaster (0-14). Tentukan label topik akademis yang cocok untuk masing-masing klaster.

- [ ] **Step 3: Tulis file pemetaan JSON**
Buat file `01_Clustering_and_Labelling/cluster_names.json` yang berisi mapping berupa dictionary:
```json
{
  "0": "Nama Bidang 0",
  "1": "Nama Bidang 1",
  ...
  "14": "Nama Bidang 14"
}
```

- [ ] **Step 4: Bersihkan script sementara & Commit**
Hapus `read_outputs.py` dan commit `cluster_names.json` ke Git.
