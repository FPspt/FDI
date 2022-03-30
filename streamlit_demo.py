import streamlit as st
from multipage import MultiPage
from pages import description, importData, FDI_Cleanser

app = MultiPage()

st.title("Future Disruption Index")

app.add_page("Future Disruption Index", description.app)
app.add_page("FDI Cleanser", FDI_Cleanser.app)


app.run()