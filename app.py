import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Kertas Kerja Santunan Meninggal")
st.write("""File ini berisikan Anomali Santunan Meninggal.xlsx""")


# Fungsi untuk membaca file Excel yang diunggah
uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])
if uploaded_file:
    # Baca kedua lembar dari file Excel
    sheet1 = pd.read_excel(uploaded_file, sheet_name="Anggota", dtype=str)
    sheet2 = pd.read_excel(uploaded_file, sheet_name="Suami", dtype=str)

    # Gabungkan data
    combined_data = pd.concat([sheet1, sheet2], ignore_index=True)

    # Tambahkan kolom tambahan
    combined_data["Kelengkapan Dokumen"] = ""
    combined_data["Hasil Konfirmasi"] = ""
    combined_data["Keterangan (Kelemahan)"] = ""

    # Format ulang kolom tanggal ke DD/MM/YYYY
    date_columns = [
        "Tgl. Gabung", "TANGGAL CAIR", "TANGGAL ACC DNR"
    ]
    for col in date_columns:
        combined_data[col] = pd.to_datetime(combined_data[col], errors="coerce").dt.strftime("%d/%m/%Y")

    # Urutkan ulang kolom 'No.'
    combined_data["No"] = range(1, len(combined_data) + 1)

    # Tampilkan data gabungan di Streamlit
    st.write("Data gabungan:")
    st.dataframe(combined_data)

    # Fungsi untuk menyimpan DataFrame ke dalam format Excel
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Gabungan")
        processed_data = output.getvalue()
        return processed_data

    # Konversi data ke Excel
    excel_data = convert_df_to_excel(combined_data)

    # Tombol untuk mengunduh file Excel
    st.download_button(
        label="Unduh Data Gabungan",
        data=excel_data,
        file_name="Data_Gabungan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
