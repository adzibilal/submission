# Air Quality Dashboard ✨

## Struktur Folder
```
dashboard/
│
├── all_data.csv                    # File CSV yang mengandung semua data gabungan
├── combine_data.py                 # Script untuk menggabungkan data dari beberapa file CSV
├── dashboard.py                     # Script utama untuk menjalankan aplikasi Streamlit
│
data/
```

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
mkdir air_quality_dashboard
cd air_quality_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run .\dashboard\dashboard.py
```

## Copyright
© 2024 Adzi Bilal M H
