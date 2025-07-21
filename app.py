import streamlit as st
import pandas as pd
import os

DATA_FILE = "aset_data.csv"

# === Load data CSV (buat file kosong kalau belum ada) ===

st.set_page_config(page_title="Monitoring Aset Perhutani", layout="wide")
st.title("📊 Monitoring Aset Perhutani")

# === Form Input ===
st.subheader("➕ Tambah Data Aset")

with st.form("form_aset"):
    kph = st.text_input("Nama KPH")
    jenis = st.selectbox("Jenis Aset", ["Tanah", "Bangunan", "Kendaraan", "Peralatan"])
    nama = st.text_input("Nama Aset")
    nilai = st.number_input("Nilai Perolehan (Rp)", min_value=0)
    tahun = st.number_input("Tahun Perolehan", min_value=1900, max_value=2100, value=2024)
    kondisi = st.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"])
    submit = st.form_submit_button("💾 Simpan")

    if submit:
        if kph and nama and nilai > 0:
            new_data = pd.DataFrame([[kph, jenis, nama, nilai, tahun, kondisi]],
                                    columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Data berhasil disimpan!")
        else:
            st.error("⚠️ Harap isi semua data sebelum menyimpan.")

# === Dashboard ===
st.subheader("📈 Dashboard Aset")

if not df.empty:
    # Ringkasan
    col1, col2 = st.columns(2)
    col1.metric("Total Aset", len(df))
    col2.metric("Total Nilai (Rp)", f"{df['Nilai Perolehan'].sum():,.0f}")

    # Filter
    st.sidebar.header("🔎 Filter Data")
    kph_filter = st.sidebar.multiselect("Filter KPH", df["KPH"].unique())
    jenis_filter = st.sidebar.multiselect("Filter Jenis Aset", df["Jenis Aset"].unique())

    filtered_df = df.copy()
    if kph_filter:
        filtered_df = filtered_df[filtered_df["KPH"].isin(kph_filter)]
    if jenis_filter:
        filtered_df = filtered_df[filtered_df["Jenis Aset"].isin(jenis_filter)]

    # Grafik distribusi per jenis
    st.subheader("Distribusi Nilai Aset per Jenis")
    if not filtered_df.empty:
        st.bar_chart(filtered_df.groupby("Jenis Aset")["Nilai Perolehan"].sum())
    else:
        st.info("Tidak ada data sesuai filter.")

    # Grafik distribusi per KPH
    st.subheader("Distribusi Nilai Aset per KPH")
    if not filtered_df.empty:
        st.bar_chart(filtered_df.groupby("KPH")["Nilai Perolehan"].sum())
    else:
        st.info("Tidak ada data sesuai filter.")

    # Tabel detail
    st.subheader("📋 Data Detail")
    st.dataframe(filtered_df)

    # Download data
    st.download_button(
        label="⬇️ Download Data CSV",
        data=filtered_df.to_csv(index=False),
        file_name="aset_data_download.csv",
        mime="text/csv"
    )
else:
    st.info("Belum ada data aset. Silakan input dulu di form di atas.")
