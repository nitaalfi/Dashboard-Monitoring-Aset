import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Aset dari File", layout="wide")
st.title("📊 Monitoring Aset Perhutani dari File Excel/CSV")

# === Upload file ===
uploaded_file = st.file_uploader("📂 Upload file Excel/CSV aset", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Deteksi format file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        # Kalau Excel, ambil sheet pertama pakai openpyxl
        xls = pd.ExcelFile(uploaded_file, engine="openpyxl")
        sheet_name = xls.sheet_names[0]  # ambil sheet pertama
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine="openpyxl")

    st.success(f"✅ Data dari `{uploaded_file.name}` berhasil dimuat!")
    
    # Preview data
    st.subheader("📋 Preview Data")
    st.dataframe(df.head())

    # Cek kolom penting
    required_cols = ["KPH", "Jenis", "Nama", "Nilai", "Tahun", "Kondisi"]
    matched_cols = [col for col in df.columns if any(req.lower() in col.lower() for req in required_cols)]
    
    if len(matched_cols) >= 4:
        # Cari kolom nilai (yang ada kata "nilai")
        nilai_col = next((c for c in df.columns if "nilai" in c.lower()), None)
        if nilai_col:
            df[nilai_col] = pd.to_numeric(df[nilai_col], errors="coerce").fillna(0)

        # Ringkasan
        col1, col2 = st.columns(2)
        col1.metric("Total Aset", len(df))
        if nilai_col:
            col2.metric("Total Nilai (Rp)", f"{df[nilai_col].sum():,.0f}")

        # Cari kolom KPH & Jenis
        kph_col = next((c for c in df.columns if "kph" in c.lower()), None)
        jenis_col = next((c for c in df.columns if "jenis" in c.lower()), None)
        
        # Filter sidebar
        st.sidebar.header("🔎 Filter Data")
        filtered_df = df.copy()
        if kph_col:
            kph_filter = st.sidebar.multiselect("Filter KPH", df[kph_col].dropna().unique())
            if kph_filter:
                filtered_df = filtered_df[filtered_df[kph_col].isin(kph_filter)]
        if jenis_col:
            jenis_filter = st.sidebar.multiselect("Filter Jenis Aset", df[jenis_col].dropna().unique())
            if jenis_filter:
                filtered_df = filtered_df[filtered_df[jenis_col].isin(jenis_filter)]

        # Grafik distribusi per jenis
        if jenis_col and nilai_col:
            st.subheader("Distribusi Nilai Aset per Jenis")
            st.bar_chart(filtered_df.groupby(jenis_col)[nilai_col].sum())
        
        # Grafik distribusi per KPH
        if kph_col and nilai_col:
            st.subheader("Distribusi Nilai Aset per KPH")
            st.bar_chart(filtered_df.groupby(kph_col)[nilai_col].sum())

        # Tabel detail
        st.subheader("📋 Data Detail")
        st.dataframe(filtered_df)

        # Download filtered data
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_aset_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Kolom tidak sesuai format standar. Pastikan ada kolom KPH, Jenis Aset, Nilai Perolehan, Tahun, Kondisi.")

else:
    st.info("Silakan upload file Excel/CSV untuk melihat dashboard.")