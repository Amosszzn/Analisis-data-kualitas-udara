# Air Quality Analysis Dashboard 🌬️

## Deskripsi Proyek
Proyek ini berisi penganalisisan data kualitas udara di berbagai stasiun pemantauan di Beijing. Fokus utamanya adalah memahami bagaimana kondisi cuaca (seperti hujan) memengaruhi kadar polutan PM2.5 dan bagaimana pola harian emisi NO2 di wilayah perkotaan (urban).

## Struktur Folder
- `/dashboard`: Berisi file utama dashboard (`dashboard.py`) dan dataset yang telah dibersihkan (`main_data.csv`).
- `/data`: Berisi kumpulan dataset mentah (CSV) dari berbagai stasiun.
- `notebook.ipynb`: File Jupyter Notebook untuk proses analisis data (Wrangling, EDA, Visualisasi).
- `requirements.txt`: Daftar library Python yang dibutuhkan untuk menjalankan proyek.
- `README.md`: Dokumentasi proyek.

## Setup Environment - Anaconda
```bash 
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt```


## Setup Environment - Shell/Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt```


## Run Steamlit App
```bash streamlit run dashboard/dashboard.py```