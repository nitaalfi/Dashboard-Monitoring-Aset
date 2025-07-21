import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Monitoring Aset", layout="wide")

st.title("📊 Dashboard Monitoring Aset Perhutani")

# ======================
# Fungsi Load Data
# ======================
def load_excel(file):
    # Skip 1 baris awal biar header rapi
    df = pd.read_excel(file, skiprows=1)
    
    # Hapus kolom "Unnamed"
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    
    # Bersihkan nama kolom
    df.columns = df.columns.str.strip()
    
    # Mapping nama kolom biar konsisten
    column_mapping = {
        "Nama Aset*": "Nama Aset",
        "Nomor Aset*": "Nomor Aset",
        "Tanggal Perolehan*": "Tahun",
        "Nilai Perolehan*": "Nilai Perolehan",
        "Kondisi Aset*": "Kondisi Aset",
        "Alamat": "Alamat"
    }
    df.rename(columns=column_mapping, inplace=True)

    # Pastikan kolom minimal ada
    important_cols = ["Nama Aset", "Nomor Aset", "Tahun", "Nilai Perolehan", "Kondisi Aset", "Alamat"]
    for col in important_cols:
        if col not in df.columns:
            df[col] = None  # kalau kolom hilang, tambahkan kosong

    # Bersihkan nilai numerik
    if "Nilai Perolehan" in df.columns:
        df["Nilai Perolehan"] = (
            df["Nilai Perolehan"]
            .astype(str)
            .str.replace(r"[^0-9]", "", regex=True)  # hanya angka
        )
        df["Nilai Perolehan"] = pd.to_numeric(df["Nilai Perolehan"], errors="coerce").fillna(0)

    return df

# ======================
# Upload File
# ======================
uploaded_file = st.file_uploader("📂 Upload File Excel Aset", type=["xlsx"])

if uploaded_file:
    df = load_excel(uploaded_file)

    st.success(f"✅ Data dari **{uploaded_file.name}** berhasil dimuat!")
    
    # ======================
    # Preview Data
    # ======================
    st.subheader("📋 Preview Data")
    st.dataframe(df.head(10))

    # ======================
    # Statistik Ringkas
    # ======================
    st.subheader("📈 Statistik Nilai Aset")
    total_aset = len(df)
    total_nilai = df["Nilai Perolehan"].sum()
    kondisi_unik = df["Kondisi Aset"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Aset", total_aset)
    col2.metric("Total Nilai Perolehan", f"Rp {total_nilai:,.0f}")
    col3.metric("Jumlah Kondisi Unik", kondisi_unik)

    # ======================
    # Visualisasi
    # ======================
    st.subheader("📊 Visualisasi Data")

    # Grafik nilai per kondisi aset
    if "Kondisi Aset" in df.columns:
        fig_kondisi = px.histogram(df, x="Kondisi Aset", y="Nilai Perolehan",
                                   title="Total Nilai Perolehan per Kondisi Aset",
                                   text_auto=True)
        st.plotly_chart(fig_kondisi, use_container_width=True)

    # Grafik distribusi aset berdasarkan tahun perolehan
    if "Tahun" in df.columns:
        # Convert ke tahun aja
        df["Tahun Perolehan"] = pd.to_datetime(df["Tahun"], errors="coerce").dt.year
        fig_tahun = px.histogram(df, x="Tahun Perolehan",
                                 title="Distribusi Jumlah Aset per Tahun Perolehan")
        st.plotly_chart(fig_tahun, use_container_width=True)

else:
    st.info("👆 Silakan upload file Excel aset terlebih dahulu.")
