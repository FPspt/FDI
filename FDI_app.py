import streamlit as st
from multipage import MultiPage
from pages import FDI_Main, FDI_Feed_Score, FDI_CoOccurence, FDI_Investor_Score

app = MultiPage()

st.title("Future Disruption Index")

app.add_page("Future Disruption Index", FDI_Main.app)
app.add_page("FDI Feed Score", FDI_Feed_Score.app)
app.add_page(" -> FDI Co-Occurence Calculator", FDI_CoOccurence.app)
app.add_page("FDI Investor Score",FDI_Investor_Score.app)
#app.add_page("FDI Cleanser", FDI_Cleanser.app)

app.run()
