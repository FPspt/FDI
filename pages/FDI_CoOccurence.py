import streamlit as st
import pandas as pd 
from utils import calculate_coOccur, filter_feed_score_by_time

def app(lower_bound,upper_bound):
    data = pd.read_excel('asset/FDI_Raw.xlsx')
    deduplicate_lv2_to_lv1 = pd.read_excel('asset/Feed_Deduplicate_FeedLV2_To_FeedLV1.xlsx')

    companyFeedLV1 = list(set(deduplicate_lv2_to_lv1['Deduplicated Feeds (LV1)'].values))

    col1, col2 = st.columns([1,3])
    with col1:
        co_occurwith = st.multiselect('Search feeds Co-Occuring with',companyFeedLV1)
    with col2:
        time = st.slider("Select the Period of Time",
                                value=(lower_bound,upper_bound),
                                format="MM/DD/YY")
        data = filter_feed_score_by_time(data,time[0],time[1])

    if co_occurwith:
        df = calculate_coOccur(data,co_occurwith)
        st.dataframe(df)