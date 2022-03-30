import streamlit as st
import pandas as pd
from collections import Counter
def app():
    unicorns = pd.read_excel('asset/UnicornsSince2010.xlsx')
    unicorn_investors = [_ for sublist in unicorns['Institutional Investors'] if type(sublist) is str for _ in sublist.split('\n')]
    unicorn_investors_count = Counter(unicorn_investors).most_common()
    df = pd.DataFrame(unicorn_investors_count)
    st.dataframe(df)