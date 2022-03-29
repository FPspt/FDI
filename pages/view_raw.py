import streamlit as st
import pandas as pd
import pickle
from utils import prevent_break, json_to_excel, to_excel, deduplicate_data

def app():
    select = st.selectbox('Please choose the timeframe you are willing to view.',
                                ['2019.08.01 ~ 2020.01.31', 
                                 '2020.08.01 ~ 2021.01.31',
                                 '2021.08.01 ~ 2022.01.31'])

    data_path = {"2019.08.01 ~ 2020.01.31": "pages/data/(190801~200131)Top100 Investments.bin",
                 "2020.08.01 ~ 2021.01.31": "pages/data/(200801~210131)Top100 Investments.bin",
                 "2021.08.01 ~ 2022.01.31": "pages/data/(210801~220131)Top100 Investments.bin"}

    with open(data_path[select], 'rb') as file:
        data = pickle.load(file)
    
    data_df = deduplicate_data(json_to_excel(data))
    st.dataframe(data_df)
    st.download_button(label='📥 Download Current Result',
                            data=to_excel(data_df) ,
                            file_name= 'FDI_{select}_Investments_Raw.xlsx')

        

