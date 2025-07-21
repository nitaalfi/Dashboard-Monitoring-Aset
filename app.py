import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Monitoring Aset", layout="wide")

st.title("📊 Dashboard Monitoring Aset Perhutani")

# ========================
# Upload File Excel
# ========================
uploaded_file = st.file_uploader("📂 Upload file Excel aset (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Load Excel
        df = pd.read_excel(uploaded_file)

        st.success(f"✅ Data dari **{uploaded_file.name}** berhasil dimuat!")

        # ========================
        # Preview Data
        # ========================
        st.subheader("📝 Preview Data")
        st.dataframe(df.head(20))

        # ========================
        # Validasi Kolom
        # ========================
        required_cols = ["KPH", "Jenis Aset", "Nilai Perolehan*", "Tahun", "Kondisi Aset*"]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.warning(f"⚠️ Kolom berikut hilang: {', '.join(missing_cols)}")
        else:
            st.success("✅ Semua kolom penting ditemukan!")

            # ========================
            # Bersihkan Kolom Nilai Perolehan
            # ========================
            st.subheader("📈 Statistik Nilai Aset")

            df["Nilai Perolehan Bersih"] = (
                df["Nilai Perolehan*"]
                .astype(str)  # pastikan string
                .str.replace(r"[^0-9.,]", "", regex=True)  # hapus semua huruf & simbol selain angka
                .str.replace(",", ".", regex=False)  # ganti koma jadi titik
            )
            df["Nilai Perolehan Bersih"] = pd.to_numeric(df["Nilai Perolehan Bersih"], errors="coerce")

            # Hitung statistik
            total_aset = df["Nilai Perolehan Bersih"].sum(skipna=True)
            rata2_aset = df["Nilai Perolehan Bersih"].mean(skipna=True)
            jumlah_valid = df["Nilai Perolehan Bersih"].count()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Nilai Aset", f"Rp {total_aset:,.0f}")
            col2.metric("Rata-rata Nilai Aset", f"Rp {rata2_aset:,.0f}")
            col3.metric("Jumlah Data Valid", f"{jumlah_valid} aset")

            # ========================
            # Visualisasi Distribusi
            # ========================
            st.subheader("📊 Distribusi Nilai Aset (Valid)")
            valid_data = df[df["Nilai Perolehan Bersih"].notna()]
            fig = px.histogram(valid_data, x="Nilai Perolehan Bersih", nbins=30,
                               title="Distribusi Nilai Aset",
                               labels={"Nilai Perolehan Bersih": "Nilai (Rp)"})
            st.plotly_chart(fig, use_container_width=True)

            # ========================
            # Ringkasan Kondisi Aset
            # ========================
            st.subheader("🏷️ Kondisi Aset")
            kondisi_count = df["Kondisi Aset*"].value_counts()
            st.bar_chart(kondisi_count)

            # ========================
            # Ringkasan per KPH
            # ========================
            st.subheader("📍 Ringkasan per KPH")
            if "KPH" in df.columns:
                kph_summary = df.groupby("KPH")["Nilai Perolehan Bersih"].sum().sort_values(ascending=False)
                st.dataframe(kph_summary)

                fig_kph = px.bar(kph_summary, title="Total Nilai Aset per KPH")
                st.plotly_chart(fig_kph, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Gagal memuat file: {e}")

else:
    st.info("⬆️ Silakan upload file Excel aset untuk mulai analisis.")
