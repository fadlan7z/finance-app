import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Utama
st.set_page_config(page_title="Monitor Keuangan Online", layout="wide")
st.title("💸 Dashboard Keuangan Real-Time")

# Membaca file Laporan_Keuangan_Lengkap_Final.xlsx
@st.cache_data
def load_data():
    file = "Laporan_Keuangan_Lengkap_Final.xlsx"
    df_kas = pd.read_excel(file, sheet_name='Buku Kas')
    df_ringkasan = pd.read_excel(file, sheet_name='Neraca & Ringkasan')
    return df_kas, df_ringkasan

df_kas, df_ringkasan = load_data()

# --- BAGIAN RINGKASAN ATAS ---
st.subheader("Ringkasan Saldo")
# Mengambil nilai dari sheet Neraca & Ringkasan
pemasukan = df_ringkasan.iloc[0, 1]
pengeluaran = df_ringkasan.iloc[1, 1]
saldo = df_ringkasan.iloc[2, 1]

c1, c2, c3 = st.columns(3)
c1.metric("Total Pemasukan", f"Rp {pemasukan:,.0f}")
c2.metric("Total Pengeluaran", f"Rp {pengeluaran:,.0f}")
c3.metric("Sisa Saldo", f"Rp {saldo:,.0f}")

st.divider()

# --- VISUALISASI ---
col_left, col_right = st.columns(2)

with col_left:
    st.write("**Detail Transaksi Terakhir**")
    # Menampilkan tabel Buku Kas
    st.dataframe(df_kas.dropna(subset=['Tanggal']).head(10), use_container_width=True)

with col_right:
    st.write("**Porsi Pengeluaran per Kategori**")
    # Plotting data dari kolom kategori
    df_pie = df_ringkasan.iloc[:, 3:5].dropna()
    df_pie.columns = ['Kategori', 'Nilai']
    fig = px.pie(df_pie, values='Nilai', names='Kategori', hole=0.3)
    st.plotly_chart(fig, use_container_width=True)