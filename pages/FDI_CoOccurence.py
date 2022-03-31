import streamlit as st
import pandas as pd 
from utils import calculate_coOccur

def app():
    data = pd.read_excel('asset/FDI_Raw.xlsx')
    deduplicate_lv2_to_lv1 = pd.read_excel('asset/Feed_Deduplicate_FeedLV2_To_FeedLV1.xlsx')

    companyFeedLV1 = list(set(deduplicate_lv2_to_lv1['Deduplicated Feeds (LV1)'].values))
    co_occurwith = st.multiselect('Search feeds Co-Occuring with',companyFeedLV1)

    if co_occurwith:
        df = calculate_coOccur(data,co_occurwith)
        st.dataframe(df)