import streamlit as st
from multipage import MultiPage
from datetime import datetime
from pages import FDI_Main, FDI_Feed_Score, FDI_CoOccurence, FDI_Investor_Score, FDI_Cleanser

app = MultiPage()
st.set_page_config(layout="wide")

st.title("Future Disruption Index")

lower_bound = datetime(2019,1,1)
upper_bound = datetime(2022,3,1)

app.add_page("Future Disruption Index", FDI_Main.app)
app.add_page("FDI Feed Score", FDI_Feed_Score.app)
app.add_page(" -> FDI Co-Occurence Calculator", FDI_CoOccurence.app(lower_bound,upper_bound))
app.add_page("FDI Investor Score",FDI_Investor_Score.app)
app.add_page("Cleanse File",FDI_Cleanser.app)
#app.add_page("FDI Cleanser", FDI_Cleanser.app)

app.run()
