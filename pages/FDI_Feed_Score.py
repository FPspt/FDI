import streamlit as st
import pandas as pd

def app():
    with open("pages/FDI_Feed_Score.md") as f:
        st.markdown(f.read())

    col1,col2,col3 = st.beta_columns([3,1,1])
    with col1:
        st.write('About to be added.')
    with col2:
        top_n = st.slider('Top_N Investors', 0, 100, 10)
    with col3:
        top_n = st.slider('Top_N Investors', 0, 100, 10)