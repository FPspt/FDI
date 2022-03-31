import streamlit as st
import pandas as pd
from utils import calculate_feed_score_ratio

def app():
    with open("pages/FDI_Feed_Score.md") as f:
        st.markdown(f.read())

    data = pd.read_excel('asset/FDI_raw.xlsx')
    col1,col2,col3 = st.columns([2,1,1])
    with col1:
        st.write('About to be added.')
    with col2:
        top_n_col2 = st.slider('Top_N Investors', 0, 100, 10, key='col2_slider')
        col2_df = calculate_feed_score_ratio(data,top_n_col2)
        st.dataframe(col2_df)
    with col3:
        top_n_col3 = st.slider('Top_N Investors', 0, 100, 10, key='col3_slider')
        col3_df = calculate_feed_score_ratio(data,top_n_col3)
        st.dataframe(col3_df)