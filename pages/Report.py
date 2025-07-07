import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="InsightBox",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded", 
)
st.title("Genearate a report 📄")

st.sidebar.title("Actions")
st.sidebar.page_link("main.py", label="Home", icon="🔍")
st.sidebar.page_link("pages/Explore.py", label="Explore Data", icon="🔍")
st.sidebar.page_link("pages/Clean.py", label="Clean Data ", icon="🧼")
st.sidebar.page_link("pages/Transform.py", label="Transform Columns", icon="🔀")
st.sidebar.page_link("pages/Statistical.py", label="Statistical Analysis", icon="📊")
st.sidebar.page_link("pages/Visualization.py", label="Data Visualization", icon="📈")
st.sidebar.page_link("pages/Prediction.py", label="Prediction", icon="🤖", disabled=True)
st.sidebar.page_link("pages/Report.py", label="Generate Report", icon="📄")