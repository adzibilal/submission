import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Membaca data dari all_data.csv
main_data = pd.read_csv('dashboard/all_data.csv')

# Membuat kolom musim berdasarkan bulan
def assign_season(month):
    if month in [3, 4, 5]:
        return 'Musim Semi'
    elif month in [6, 7, 8]:
        return 'Musim Panas'
    elif month in [9, 10, 11]:
        return 'Musim Gugur'
    else:
        return 'Musim Dingin'

# Tambahkan kolom 'SEASON' ke dalam data
main_data['SEASON'] = main_data['month'].apply(assign_season)

# Menampilkan judul
st.title("Dashboard Kualitas Udara")

# Menampilkan deskripsi
st.write("""
    Dashboard ini memberikan wawasan tentang kualitas udara berdasarkan data dari berbagai stasiun.
    Anda dapat menjelajahi distribusi polutan, hubungan antara variabel, dan banyak lagi.
""")

data = main_data

# Pilihan untuk visualisasi
visualization_type = st.selectbox("Pilih Jenis Visualisasi:",
                                   ("Pengaruh Musim Terhadap Suhu","Perbandingan Suhu Antar Stasiun","Trend Waktu Polutan Utama (PM2.5 dan PM10)","Heatmap Hubungan Antara Polutan dan Variabel Cuaca","Polusi Berdasarkan Stasiun dan Arah Angin","Distribusi PM2.5", "Distribusi PM10", "PM2.5 vs Curah Hujan", "PM2.5 vs Suhu"))

# Penggunaan Selectbox adalah untuk meningkatkan performa dashboard, mengingat jumlah data yang ada 300rb baris lebih

# Menampilkan visualisasi berdasarkan pilihan
if visualization_type == "Pengaruh Musim Terhadap Suhu":
    st.subheader("Pengaruh Musim Terhadap Suhu")

    # Menghitung suhu rata-rata per musim
    avg_temp_per_season = main_data.groupby('SEASON')['TEMP'].mean().reindex(
        ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])

    # Membuat bar plot
    plt.figure(figsize=(8, 6))
    sns.barplot(x=avg_temp_per_season.index, y=avg_temp_per_season.values, palette='coolwarm')

    # Menambahkan judul dan label
    plt.title('Rata-rata Suhu per Musim', fontsize=16)
    plt.xlabel('Musim', fontsize=12)
    plt.ylabel('Suhu Rata-rata (°C)', fontsize=12)
    plt.grid(axis='y')
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
elif visualization_type == "Perbandingan Suhu Antar Stasiun":
    st.subheader("Perbandingan Suhu Antar Stasiun")

    # Membuat boxplot suhu berdasarkan stasiun
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=main_data, x='station', y='TEMP', palette='coolwarm')

    # Menambahkan judul dan label
    plt.title('Perbandingan Suhu Antar Stasiun', fontsize=16)
    plt.xlabel('Stasiun', fontsize=12)
    plt.ylabel('Suhu (°C)', fontsize=12)
    plt.xticks(rotation=45)  # Memiringkan label stasiun agar lebih mudah dibaca
    plt.grid(axis='y')
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
elif visualization_type == "Trend Waktu Polutan Utama (PM2.5 dan PM10)":
    st.subheader("Trend Waktu Polutan Utama (PM2.5 dan PM10)")

    # Mengelompokkan data berdasarkan bulan dan menghitung rata-rata PM2.5 dan PM10
    monthly_avg_pollutants = main_data.groupby(['year', 'month'])[['PM2.5', 'PM10']].mean().reset_index()

    # Menggabungkan kolom tahun dan bulan menjadi satu kolom datetime untuk tren waktu
    monthly_avg_pollutants['date'] = pd.to_datetime(monthly_avg_pollutants[['year', 'month']].assign(day=1))

    # Plot garis untuk PM2.5 dan PM10
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg_pollutants['date'], monthly_avg_pollutants['PM2.5'], label='PM2.5', color='blue', marker='o')
    plt.plot(monthly_avg_pollutants['date'], monthly_avg_pollutants['PM10'], label='PM10', color='orange', marker='o')

    # Menambahkan judul, label, dan legenda
    plt.title('Trend Waktu Polutan Utama (PM2.5 dan PM10)', fontsize=16)
    plt.xlabel('Waktu', fontsize=12)
    plt.ylabel('Konsentrasi Polutan (µg/m³)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
elif visualization_type == "Heatmap Hubungan Antara Polutan dan Variabel Cuaca":
    st.subheader("Heatmap Hubungan Antara Polutan dan Variabel Cuaca")

    # Menghitung korelasi antara kolom polutan dan variabel cuaca
    correlation_matrix = main_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']].corr()

    # Membuat heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})

    # Menambahkan judul
    plt.title('Heatmap Hubungan Antara Polutan dan Variabel Cuaca', fontsize=16)
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
elif visualization_type == "Polusi Berdasarkan Stasiun dan Arah Angin":
    st.subheader("Wind Rose Plot: Polusi Berdasarkan Stasiun dan Arah Angin")

    # Menyiapkan data untuk Wind Rose Plot
    wind_data = main_data['wd'].value_counts().reset_index()
    wind_data.columns = ['Direction', 'Frequency']

    # Pastikan untuk hanya menggunakan arah angin yang valid
    valid_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW',
                        'NNW']
    wind_data = wind_data[wind_data['Direction'].isin(valid_directions)]

    # Membuat plot
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, polar=True)
    angles = np.linspace(0, 2 * np.pi, len(wind_data), endpoint=False).tolist()
    angles += angles[:1]
    values = wind_data['Frequency'].tolist()
    values += values[:1]

    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(wind_data['Direction'])
    ax.set_title('Wind Rose Plot')

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
elif visualization_type == "Distribusi PM2.5":
    st.subheader("Distribusi PM2.5")
    plt.figure(figsize=(8, 5))

    # Membuat histogram untuk distribusi PM2.5
    sns.histplot(data['PM2.5'].dropna(), bins=20, kde=True, color='blue')
    plt.title('Distribusi PM2.5')
    plt.xlabel('Konsentrasi PM2.5 (µg/m³)')
    plt.ylabel('Frekuensi')
    plt.grid()
    st.pyplot(plt)

elif visualization_type == "Distribusi PM10":
    st.subheader("Distribusi PM10")
    plt.figure(figsize=(8, 5))

    # Membuat histogram untuk distribusi PM10
    sns.histplot(data['PM10'].dropna(), bins=20, kde=True, color='orange')
    plt.title('Distribusi PM10')
    plt.xlabel('Konsentrasi PM10 (µg/m³)')
    plt.ylabel('Frekuensi')
    plt.grid()
    st.pyplot(plt)

elif visualization_type == "PM2.5 vs Curah Hujan":
    st.subheader("PM2.5 vs Curah Hujan")
    plt.figure(figsize=(8, 5))

    # Membuat scatter plot antara curah hujan dan PM2.5
    sns.scatterplot(data=data, x='RAIN', y='PM2.5', color='green')
    plt.title('PM2.5 vs Curah Hujan (RAIN)')
    plt.xlabel('Curah Hujan (mm)')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    plt.grid()
    st.pyplot(plt)

elif visualization_type == "PM2.5 vs Suhu":
    st.subheader("PM2.5 vs Suhu")
    plt.figure(figsize=(8, 5))

    # Membuat scatter plot antara suhu dan PM2.5
    sns.scatterplot(data=data, x='TEMP', y='PM2.5', color='red')
    plt.title('PM2.5 vs Suhu (TEMP)')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    plt.grid()
    st.pyplot(plt)

# Menambahkan glosarium
st.subheader("Glosarium")
st.write("""
- **PM2.5**: Konsentrasi partikel debu halus yang berukuran kurang dari 2.5 mikrometer, diukur dalam mikrogram per meter kubik (µg/m³).
- **PM10**: Konsentrasi partikel debu kasar yang berukuran kurang dari 10 mikrometer, diukur dalam mikrogram per meter kubik (µg/m³).
- **SO2**: Konsentrasi sulfur dioksida, gas polutan yang berbahaya bagi kesehatan, diukur dalam mikrogram per meter kubik (µg/m³).
- **NO2**: Konsentrasi nitrogen dioksida, gas polutan yang berasal dari pembakaran bahan bakar, diukur dalam mikrogram per meter kubik (µg/m³).
- **CO**: Konsentrasi karbon monoksida, gas beracun hasil pembakaran yang tidak sempurna, diukur dalam miligram per meter kubik (mg/m³).
- **O3**: Konsentrasi ozon, gas yang ada di lapisan atmosfer dan dapat bersifat polutan di permukaan tanah, diukur dalam mikrogram per meter kubik (µg/m³).
- **TEMP**: Suhu udara pada saat pengambilan data, diukur dalam derajat Celsius (°C).
- **PRES**: Tekanan atmosfer pada saat pengambilan data, diukur dalam hektoPascal (hPa).
- **DEWP**: Suhu titik embun pada saat pengambilan data, yaitu suhu di mana uap air di udara mulai mengembun, diukur dalam derajat Celsius (°C).
- **RAIN**: Curah hujan pada saat pengambilan data, diukur dalam milimeter (mm).
- **wd**: Arah angin, ditunjukkan dengan singkatan arah kompas (misalnya, N untuk Utara, NW untuk Barat Laut, dsb).
- **WSPM**: Kecepatan angin, diukur dalam meter per detik (m/s).
""")

# caption copyright

st.caption("© 2024. Dibuat oleh [Adzi Bilal](https://www.linkedin.com/in/adzibilal/)")