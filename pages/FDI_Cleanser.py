import streamlit as st
import pandas as pd
from utils import tracxn_export_to_fdi, to_excel,deduplicate_data

def app():
    with open("pages/FDI_Cleanser.md") as f:
        st.markdown(f.read())

    uploaded_files = st.file_uploader("Choose a XLSX file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        name = uploaded_file.name.replace('.xlsx','')
        uploaded_file_df = pd.read_excel(uploaded_file)
        
        uploaded_file_fdi = tracxn_export_to_fdi(uploaded_file_df)
        uploaded_file_dedupicated = deduplicate_data(uploaded_file_fdi)

        st.dataframe(uploaded_file_dedupicated)
        st.download_button(label='📥 Download Current Result',
                                data=to_excel(uploaded_file_dedupicated) ,
                                file_name= f'{name}_FDI_Cleansed.xlsx')