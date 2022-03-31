import streamlit as st
import pandas as pd
from datetime import datetime
from utils import calculate_feed_score, to_excel, filter_feed_score_by_time

def app():
    with open("pages/FDI_Feed_Score.md") as f:
        st.markdown(f.read())

    data  = pd.read_excel('asset/FDI_raw.xlsx')
    score = pd.read_excel('asset/A_22H1_Investor Score.xlsx')
    
    col1, col2 = st.columns([1,3])
    with col1:
        top_n = int(st.number_input('Top N Investors', value = 100))
    with col2:
        time = st.slider("Select the Period of Time",
                                value=(datetime(2019,1,1),datetime(2022,3,1)),
                                format="MM/DD/YY")

    data = filter_feed_score_by_time(data,time[0],time[1])
    output_df = calculate_feed_score(data, score, top_n)
    cols = output_df.columns

    output_df = output_df.sort_values(by=cols[2], ascending=False)
    output_df = output_df.reset_index()

    st.dataframe(output_df,width=1200)

    st.download_button(label=f'📥 Download Current Result',
                            data=to_excel(output_df) ,
                            file_name= f'[FDI]Feed Score.xlsx')