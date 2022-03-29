import streamlit as st

def app():
    st.markdown('#### Please be aware that this page **will cost tracxn credits**.')

    if st.button("click button"):
        st.write("About to be added")