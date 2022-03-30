import streamlit as st

def app():
    st.markdown('Welcome to the Future Disruption Index(FDI) Demo page.')
    st.markdown('Powered by the Strategic Planning Team, FDI collects past data from Tracxn for early alert of emerging fields of investment. \
    For the moment, FDI leverages 30,000 past investments executed between 2018~2021 for the results.')

    # st.download_button(label='📥 Download the most recent FDI Report',
    #                             data=to_excel(uploaded_file_dedupicated),
    #                             file_name= f'{name}_FDI_Cleansed.xlsx')