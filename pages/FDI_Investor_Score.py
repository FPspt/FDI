import streamlit as st
import pandas as pd
from collections import Counter
def app():
    with open("pages/FDI_Investor_Score.md") as f:
        st.markdown(f.read())

    unicorns = pd.read_excel('asset/A_22H1_Investor Score.xlsx').astype(str)
    unicorns = unicorns.style.set_properties(**{'background-color': 'mediumturquoise'}, subset=['Final Score'])
    st.dataframe(unicorns)