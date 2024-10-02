import pandas as pd

# Membaca data
aotizhongxin_df = pd.read_csv("./data/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
changping_df = pd.read_csv("./data/PRSA_Data_Changping_20130301-20170228.csv")
dingling_df = pd.read_csv("./data/PRSA_Data_Dingling_20130301-20170228.csv")
dongsi_df = pd.read_csv("./data/PRSA_Data_Dongsi_20130301-20170228.csv")
guanyuan_df = pd.read_csv("./data/PRSA_Data_Guanyuan_20130301-20170228.csv")
huairou_df = pd.read_csv("./data/PRSA_Data_Huairou_20130301-20170228.csv")
nongzhanguan_df = pd.read_csv("./data/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
shunyi_df = pd.read_csv("./data/PRSA_Data_Shunyi_20130301-20170228.csv")
tiantan_df = pd.read_csv("./data/PRSA_Data_Tiantan_20130301-20170228.csv")
wanliu_df = pd.read_csv("./data/PRSA_Data_Wanliu_20130301-20170228.csv")
wanshouxigong_df = pd.read_csv("./data/PRSA_Data_Wanshouxigong_20130301-20170228.csv")

# Menambahkan kolom 'station' ke setiap dataframe
aotizhongxin_df['station'] = 'Aotizhongxin'
changping_df['station'] = 'Changping'
dingling_df['station'] = 'Dingling'
dongsi_df['station'] = 'Dongsi'
guanyuan_df['station'] = 'Guanyuan'
huairou_df['station'] = 'Huairou'
nongzhanguan_df['station'] = 'Nongzhanguan'
shunyi_df['station'] = 'Shunyi'
tiantan_df['station'] = 'Tiantan'
wanliu_df['station'] = 'Wanliu'
wanshouxigong_df['station'] = 'Wanshouxigong'

# Gabungkan semua dataframe
all_stations_df = pd.concat([aotizhongxin_df, changping_df, dingling_df, dongsi_df, guanyuan_df,
                             huairou_df, nongzhanguan_df, shunyi_df, tiantan_df, wanliu_df,
                             wanshouxigong_df], ignore_index=True)

# Mengisi missing values untuk kolom numerik dengan rata-rata
numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for column in numeric_columns:
    all_stations_df[column] = all_stations_df[column].fillna(all_stations_df[column].mean())

# Mengisi missing values untuk kolom kategorikal dengan modus
all_stations_df['wd'] = all_stations_df['wd'].fillna(all_stations_df['wd'].mode()[0])

# Menyimpan dataframe ke file CSV
all_stations_df.to_csv("dashboard/all_data.csv", index=False)
