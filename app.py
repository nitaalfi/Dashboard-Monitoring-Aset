import streamlit as st
import pandas as pd

# ========================
# Judul Dashboard
# ========================
st.set_page_config(page_title="Dashboard Monitoring Aset", layout="wide")
st.title("📊 Dashboard Monitoring Aset Perhutani")

st.write("Upload file Excel Master Data Aset untuk melihat monitoring.")

# ========================
# Upload File Excel
# ========================
uploaded_file = st.file_uploader("📂 Upload File Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    st.success(f"✅ File **{uploaded_file.name}** berhasil diupload")

    try:
        # Cek semua sheet di Excel
        xls = pd.ExcelFile(uploaded_file, engine="openpyxl")
        sheet_name = xls.sheet_names[0]  # ambil sheet pertama

        # Baca beberapa baris pertama untuk deteksi header
        preview_df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine="openpyxl", nrows=5)
        st.write("🔍 **Preview baris awal (untuk cek posisi header):**")
        st.dataframe(preview_df)

        # Pilihan skiprows manual
        skip_val = st.number_input("Lewati berapa baris awal? (skiprows)", min_value=0, max_value=10, value=1)

        # Baca data aset dengan skiprows yang dipilih
        df = pd.read_excel(
            uploaded_file,
            sheet_name=sheet_name,
            engine="openpyxl",
            skiprows=skip_val
        )

        st.write("### ✅ Preview Data Aset")
        st.dataframe(df.head(10))

        # ========================
        # Deteksi Kolom Utama
        # ========================
        required_cols = ["Nama Aset*", "Nomor Aset*", "Tanggal Perolehan*", "Nilai Perolehan*", "Kondisi Aset*"]
        missing_cols = [c for c in required_cols if c not in df.columns]

        if missing_cols:
            st.warning(f"⚠️ Kolom berikut tidak ditemukan: {missing_cols}")
        else:
            st.success("✅ Semua kolom penting ditemukan!")

        # ========================
        # Statistik Sederhana
        # ========================
        st.subheader("📈 Statistik Nilai Aset")
        if "Nilai Perolehan*" in df.columns:
            total_aset = df["Nilai Perolehan*"].sum()
            rata2_aset = df["Nilai Perolehan*"].mean()
            st.metric("Total Nilai Aset", f"Rp {total_aset:,.0f}")
            st.metric("Rata-rata Nilai Aset", f"Rp {rata2_aset:,.0f}")

        # ========================
        # Visualisasi Kondisi Aset
        # ========================
        if "Kondisi Aset*" in df.columns:
            st.subheader("📊 Distribusi Kondisi Aset")
            kondisi_count = df["Kondisi Aset*"].value_counts()
            st.bar_chart(kondisi_count)

        # ========================
        # Download versi bersih
        # ========================
        st.subheader("💾 Simpan Data Bersih")
        cleaned_file = "data_bersih.xlsx"
        df.to_excel(cleaned_file, index=False)
        with open(cleaned_file, "rb") as f:
            st.download_button("⬇️ Download Data Bersih", f, file_name="data_bersih.xlsx")

    except Exception as e:
        st.error(f"❌ Gagal memuat file: {e}")

else:
    st.info("Silakan upload file Excel Master Data Aset terlebih dahulu.")
