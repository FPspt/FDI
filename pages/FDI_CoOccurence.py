import streamlit as st
import pandas as pd 
from datetime import datetime
from utils import calculate_coOccur, filter_feed_score_by_time, to_excel

def app():
    with open("pages/FDI_CoOccurence.md") as f:
        st.markdown(f.read())

    data = pd.read_excel('asset/FDI_Raw.xlsx')
    deduplicate_lv2_to_lv1 = pd.read_excel('asset/Feed_Deduplicate_FeedLV2_To_FeedLV1.xlsx')

    companyFeedLV2 = list(set(deduplicate_lv2_to_lv1['Deduplicated Feeds (LV2)'].values))
    companyFeedLV1 = list(set(deduplicate_lv2_to_lv1['Deduplicated Feeds (LV1)'].values))

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        feedLV = st.selectbox('companyFeed Level', ('companyFeedLV1','companyFeedLV2'))

    with col2:
        if feedLV == 'companyFeedLV1':
            co_occurwith = st.multiselect('Search feeds Co-Occuring with',companyFeedLV1)
        else: 
            co_occurwith = st.multiselect('Search feeds Co-Occuring with',companyFeedLV2)

    with col3:
        lower_bound = datetime(2019,1,1)
        upper_bound = datetime(2022,3,1)
        time = st.slider("Select the Period of Time",
                                value=(lower_bound,upper_bound),
                                format="MM/DD/YY")
        data = filter_feed_score_by_time(data,time[0],time[1])

    if co_occurwith:
        df,tot_num = calculate_coOccur(data, co_occurwith, feedLV)
        st.write(f'Total Number: {tot_num}')
        st.dataframe(df)

        st.download_button(label='📥 Download Current Result',
                                data=to_excel(df) ,
                                file_name= f'[FDI]Co-Occurence{co_occurwith}.xlsx')