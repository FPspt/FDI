import streamlit as st
import pandas as pd
from datetime import datetime
from utils import calculate_feed_score, to_excel, filter_feed_score_by_time

def app():
    with open("pages/FDI_Feed_Score.md") as f:
        st.markdown(f.read())

    data  = pd.read_excel('asset/FDI_Raw.xlsx')
    score = pd.read_excel('asset/FDI_InvestorScore.xlsx')
    
    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        feedLV = st.selectbox('companyFeed Level', ('companyFeedLV1','companyFeedLV2'))

    with col2:
        top_n = int(st.number_input('Top N Investors', value = 100))

    with col3:
        time = st.slider("Select the Period of Time",
                                value=(datetime(2019,1,1),datetime(2022,3,1)),
                                format="MM/DD/YY")

    data = filter_feed_score_by_time(data,time[0],time[1])
    output_df = calculate_feed_score(data, score, top_n, feedLV)

    st.dataframe(output_df)

    st.download_button(label=f'📥 Download Current Result',
                            data=to_excel(output_df) ,
                            file_name= '[FDI]Feed Score.xlsx')