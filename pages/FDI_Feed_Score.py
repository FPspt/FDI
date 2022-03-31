import streamlit as st
import pandas as pd
from utils import calculate_feed_score_ratio,to_excel

def app():
    with open("pages/FDI_Feed_Score.md") as f:
        st.markdown(f.read())

    data  = pd.read_excel('asset/FDI_raw.xlsx')
    score = pd.read_excel('asset/A_22H1_Investor Score.xlsx')
    
    col2,col3 = st.columns([1,1])

    with col2:
        top_n_col2 = st.slider('Top_N Investors', 0, 100, 10, key='col2_slider')
        col2_df = calculate_feed_score_ratio(data, score, top_n_col2)
        #col2_df.drop(f'Top_{top_n_col2}_Occurence')
        #col2_df = col2_df.style.set_properties(**{'background-color': 'mediumturquoise'}, subset=[f'Top_{top_n_col2}_Ratio'])

        st.dataframe(col2_df)

        st.download_button(label=f'📥 Download Top_{top_n_col2} Feed Score',
                                data=to_excel(col2_df) ,
                                file_name= f'[FDI]Top_{top_n_col2} Feed Score.xlsx')
    with col3:
        top_n_col3 = st.slider('Top_N Investors', 0, 100, 60, key='col3_slider')
        col3_df = calculate_feed_score_ratio(data, score, top_n_col3)
        #col3_df.drop(f'Top_{top_n_col3}_Occurence')
        #col3_df = col3_df.style.set_properties(**{'background-color': 'mediumturquoise'}, subset=[f'Top_{top_n_col3}_Ratio'])

        st.dataframe(col3_df)

        st.download_button(label=f'📥 Download Top_{top_n_col3} Feed Score',
                        data=to_excel(col3_df) ,
                        file_name= f'[FDI]Top_{top_n_col3} Feed Score.xlsx')