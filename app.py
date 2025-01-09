import pandas as pd
import streamlit as st

st.title("Kertas Kerja Santunan Meninggal")
st.write("""File ini berisikan Anomali Santunan Meninggal.xlsx""")


uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])
if uploaded_file:

    sheet1 = pd.read_excel(uploaded_file, sheet_name="Anggota", dtype=str)
    sheet2 = pd.read_excel(uploaded_file, sheet_name="Suami", dtype=str)


    combined_data = pd.concat([sheet1, sheet2], ignore_index=True)


    combined_data["Kelengkapan Dokumen"] = ""
    combined_data["Hasil Konfirmasi"] = ""
    combined_data["Keterangan (Kelemahan)"] = ""


    date_columns = [
        "Tgl. Gabung", "TANGGAL CAIR", "TANGGAL KEMATIAN", "TANGGAL ACC DNR"
    ]
    for col in date_columns:
        combined_data[col] = pd.to_datetime(combined_data[col], errors="coerce").dt.strftime("%d/%m/%Y")


    combined_data["No"] = range(1, len(combined_data) + 1)


    st.write("Data gabungan:")
    st.dataframe(combined_data)


    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine="openpyxl")

    excel_data = convert_df(combined_data)

    st.download_button(
        label="Unduh KK Santunan Meninggal",
        data=excel_data,
        file_name="KK Santunan Meninggal.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )