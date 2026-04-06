import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn
sns.set(style='dark')

# Helper function untuk NO2 (Hourly)
def create_hourly_no2_df(df):
    urban_list = ['Aotizhongxin','Dongsi','Guanyuan','Nongzhanguan','Tiantan','Wanliu','Wanshouxigong']
    urban_df = df[df['station'].isin(urban_list)]
    hourly_no2_df = urban_df.groupby("hour").NO2.mean().reset_index()
    return hourly_no2_df

# Helper function untuk Dampak Hujan
def create_rain_impact_df(df):
    # Mengelompokkan berdasarkan kondisi hujan (threshold 0.1)
    df['rain_condition'] = df['RAIN'].apply(lambda x:'Rainy' if x > 0.1 else 'No Rain')
    rain_impact_df = df.groupby("rain_condition")['PM2.5'].mean().reset_index()
    return rain_impact_df

# Mendapatkan lokasi direktori tempat file dashboard.py ini berada
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "main_data.csv")

# Load data
try:
    all_df = pd.read_csv(file_path)
    all_df['datetime'] = pd.to_datetime(all_df["datetime"])
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# Membuat komponen filter di sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Error Handling untuk Date Input agar tidak unpack error
    try:
        date_range = st.date_input(
            label='Rentang Waktu',
            min_value=all_df["datetime"].min(),
            max_value=all_df['datetime'].max(),
            value=[all_df['datetime'].min(), all_df["datetime"].max()]
        )
        
        # Logika Error Handling: Pastikan ada start_date dan end_date
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            st.warning("Silakan pilih rentang waktu yang lengkap (Tanggal Mulai dan Tanggal Selesai).")
            st.stop() # Menghentikan eksekusi dashboard agar tidak muncul error merah
            
    except Exception as e:
        st.error(f"Terjadi kesalahan input tanggal: {e}")
        st.stop()

# Filter dataframe berdasarkan pilihan tanggal
main_df = all_df[(all_df['datetime'] >= pd.to_datetime(start_date)) &
                 (all_df['datetime'] <= pd.to_datetime(end_date))]

# Menyiapkan berbagai dataframe
hourly_no2_df = create_hourly_no2_df(main_df)
rain_impact_df = create_rain_impact_df(main_df)

# Header Dashboard
st.header('Air Quality Analysis Dashboard 🌬️')

# Visualisasi 1: Dampak Hujan terhadap PM2.5
st.subheader("Dampak Curah Hujan terhadap kadar PM2.5")

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#D3D3D3", "#72BCD4"]
sns.barplot(
    x="rain_condition",
    y="PM2.5",
    data=rain_impact_df,
    palette=colors,
    ax=ax
)
ax.set_title("Rata-rata Konsentrasi PM2.5 (Rainy vs No Rain)", loc="center", fontsize=15)
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.set_xlabel(None)
st.pyplot(fig)

with st.expander("Lihat detail analisis: "):
    st.write(
        """Terlihat penurunan kadar PM2.5 yang signifikan saat kondisi hujan. Ini membuktikan efek pembersihan polutan secara alami oleh air hujan di stasiun pemantauan."""
    )

# Visualisasi 2: Tren NO2 di wilayah urban
st.subheader("Tren Harian NO2 di wilayah urban")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    hourly_no2_df['hour'],
    hourly_no2_df["NO2"],
    marker="o",
    linewidth=2,
    color="#E67E22"
)
# Menambahkan shading untuk jam sibuk (contoh: 07-09 dan 17-19)
ax.axvspan(7, 9, color='yellow', alpha=0.3, label='Rush Hour Pagi')
ax.axvspan(17, 19, color='pink', alpha=0.3, label='Rush Hour Sore')

ax.set_title("Rata-rata NO2 per jam (Wilayah Urban)", loc='center')
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

with st.expander("Lihat detail analisis"):
    st.write(
        """Kadar NO2 memuncak pada jam sibuk pagi dan sore hari. Hal ini menunjukkan korelasi kuat antara emisi kendaraan bermotor dengan kualitas udara di pusat kota."""
    )

st.caption('Copyright (c) Dicoding 2024 - Proyek Akhir Analisis Data')