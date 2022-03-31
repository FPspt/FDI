import streamlit as st
import pandas as pd
from collections import Counter
def app():
    with open("pages/FDI_Investor_Score.md") as f:
        st.markdown(f.read())

    unicorns = pd.read_excel('asset/FDI_InvestorScore.xlsx').astype(str)
    st.dataframe(unicorns)