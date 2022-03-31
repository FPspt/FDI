import streamlit as st
import pandas as pd
from collections import Counter
from utils import to_excel

def app():
    with open("pages/FDI_Investor_Score.md") as f:
        st.markdown(f.read())

    unicorns = pd.read_excel('asset/FDI_InvestorScore.xlsx').astype(str)
    unicorns = unicorns[['Investor Name','Investor Domain','Investor Score']]

    st.dataframe(unicorns)
    st.download_button(label='📥 Download Current Result',
                                data=to_excel(unicorns) ,
                                file_name= '[FDI]Investor Score.xlsx')
    