import streamlit as st
import pandas as pd
from collections import Counter
def app():
    unicorns = pd.read_excel('asset/Top100Candidate_Investment_History.xlsx').astype(str)
    st.dataframe(unicorns)