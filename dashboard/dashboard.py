import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn agar visualisasi terlihat profesional
sns.set(style='ticks')

# --- FUNGSI LOAD DATA ---
def load_data():
    # Cek di folder dashboard (untuk cloud) atau folder lokal
    paths = ["dashboard/main_data.csv", "main_data.csv"]
    df = None
    
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is None:
        st.error("File 'main_data.csv' tidak ditemukan! Pastikan file ada di folder dashboard.")
        st.stop()

    # Normalisasi nama kolom ke lowercase untuk pengecekan
    cols_lower = [c.lower() for c in df.columns]
    
    # Deteksi dan gabungkan kolom waktu jika perlu
    if 'datetime' in cols_lower:
        actual_col = df.columns[cols_lower.index('datetime')]
        df.rename(columns={actual_col: 'datetime'}, inplace=True)
    elif all(k in cols_lower for k in ['year', 'month', 'day']):
        y_col = df.columns[cols_lower.index('year')]
        m_col = df.columns[cols_lower.index('month')]
        d_col = df.columns[cols_lower.index('day')]
        df['datetime'] = pd.to_datetime(df[[y_col, m_col, d_col]])
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

# Muat data di awal
main_df = load_data()

# --- SIDEBAR (Input Filter) ---
with st.sidebar:
    st.title("Air Quality Filter ☁️")
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=150)
    
    min_date = main_df["datetime"].min()
    max_date = main_df["datetime"].max()
    
    # Nilai default start dan end
    start_date, end_date = min_date, max_date
    
    # Input rentang waktu
    result = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Validasi input filter
    if isinstance(result, list) and len(result) == 2:
        start_date, end_date = result
    elif isinstance(result, list) and len(result) == 1:
        st.info("Silakan pilih tanggal akhir untuk memfilter.")

# --- FILTERING DATA ---
filtered_df = main_df[(main_df["datetime"] >= pd.to_datetime(start_date)) & 
                      (main_df["datetime"] <= pd.to_datetime(end_date))].copy()

# --- MAIN PAGE ---
st.header('Air Quality Analysis Dashboard 📊')
st.markdown(f"Menampilkan data dari: **{start_date}** hingga **{end_date}**")

# 1. Metrik Utama
col1, col2 = st.columns(2)
with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    if 'NO2' in filtered_df.columns:
        avg_no2 = filtered_df['NO2'].mean()
        st.metric("Rata-rata NO2", f"{avg_no2:.2f} µg/m³")

st.divider()

# 2. Visualisasi Dampak Hujan
st.subheader('Dampak Hujan terhadap Konsentrasi PM2.5')
if 'rain_condition' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    # Kelompokkan rata-rata PM2.5 berdasarkan kondisi hujan
    rain_data = filtered_df.groupby('rain_condition', as_index=False)['PM2.5'].mean()
    sns.barplot(x='rain_condition', y='PM2.5', data=rain_data, palette='coolwarm', ax=ax)
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_title("Perbandingan PM2.5: Hujan vs Tidak Hujan")
    st.pyplot(fig)
    st.markdown("> **Insight:** Hujan berperan sebagai pembersih alami yang menurunkan polusi PM2.5.")
else:
    st.warning("Kolom 'rain_condition' tidak ditemukan.")

# 3. Tren Kualitas Udara (Penyebab Error Sebelumnya Difiks)
st.subheader('Tren Kualitas Udara Harian (PM2.5)')
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # FIKS ERROR: Gunakan numeric_only=True agar tidak error saat ketemu kolom teks
    daily_resampled = filtered_df.set_index('datetime').resample('D').mean(numeric_only=True).reset_index()
    
    sns.lineplot(x='datetime', y='PM2.5', data=daily_resampled, color='#E67E22', ax=ax)
    
    # Fokuskan sumbu X ke rentang yang dipilih
    ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
    
    plt.xticks(rotation=45)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Konsentrasi PM2.5")
    st.pyplot(fig)
else:
    st.write("Data tidak tersedia untuk rentang ini.")

st.divider()
st.caption('Copyright © Arya Ivan Ghally 2024 - Proyek Analisis Data Dicoding')