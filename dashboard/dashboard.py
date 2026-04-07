import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set style seaborn agar visualisasi terlihat profesional
sns.set(style='ticks')

# --- FUNGSI LOAD DATA (DENGAN CACHING AGAR INTERAKTIF CEPAT) ---
@st.cache_data
def load_data():
    paths = ["dashboard/main_data.csv", "main_data.csv"]
    df = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is None:
        st.error("File 'main_data.csv' tidak ditemukan!")
        st.stop()

    # Normalisasi kolom waktu
    cols_lower = [c.lower() for c in df.columns]
    if 'datetime' in cols_lower:
        actual_col = df.columns[cols_lower.index('datetime')]
        df.rename(columns={actual_col: 'datetime'}, inplace=True)
    elif all(k in cols_lower for k in ['year', 'month', 'day']):
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day']])
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

main_df = load_data()

# --- SIDEBAR: FILTER INTERAKTIF ---
with st.sidebar:
    st.title("Air Quality Filter ☁️")
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=150)
    
    # Rentang tanggal asli dari dataset
    min_date = main_df["datetime"].min().date()
    max_date = main_df["datetime"].max().date()
    
    # Input rentang waktu (Widget Interaktif)
    try:
        start_date, end_date = st.date_input(
            label='Pilih Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Pilih rentang tanggal (Mulai & Akhir) pada kalender!")
        st.stop()

# --- PROSES FILTERING (Kunci agar Dinamis) ---
# Data inilah yang HARUS digunakan di semua grafik di bawah
filtered_df = main_df[
    (main_df["datetime"].dt.date >= start_date) & 
    (main_df["datetime"].dt.date <= end_date)
].copy()

# --- MAIN DASHBOARD ---
st.header('Air Quality Analysis Dashboard 📊')
st.markdown(f"Periode Aktif: **{start_date}** s/d **{end_date}**")

# 1. Metrik Utama (Update Otomatis)
col1, col2 = st.columns(2)
with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    if 'NO2' in filtered_df.columns:
        avg_no2 = filtered_df['NO2'].mean()
        st.metric("Rata-rata NO2", f"{avg_no2:.2f} µg/m³")

st.divider()

# 2. Grafik Bar: Dampak Hujan (Dinamis berdasarkan filtered_df)
st.subheader('Dampak Hujan terhadap Konsentrasi PM2.5')
if 'rain_condition' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    # Menggunakan filtered_df agar grafik berubah saat tanggal diganti
    rain_data = filtered_df.groupby('rain_condition', as_index=False)['PM2.5'].mean()
    sns.barplot(x='rain_condition', y='PM2.5', data=rain_data, palette='coolwarm', ax=ax)
    ax.set_ylabel("PM2.5 (µg/m³)")
    st.pyplot(fig)
else:
    st.warning("Kolom 'rain_condition' tidak ditemukan.")

# 3. Grafik Tren: (Dinamis berdasarkan filtered_df)
st.subheader('Tren Kualitas Udara Harian')
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 5))
    # Resample data yang sudah difilter
    daily_trend = filtered_df.set_index('datetime').resample('D').mean(numeric_only=True).reset_index()
    sns.lineplot(x='datetime', y='PM2.5', data=daily_trend, color='#E67E22', ax=ax)
    
    # Pastikan sumbu X mengikuti filter
    ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()
st.caption('Copyright © Arya Ivan Ghally 2024 - Proyek Analisis Data Dicoding')