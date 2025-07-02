import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualize", page_icon="📈")
st.title("📈 Data Visualizer")

if "cleaned_data" in st.session_state:
    df = st.session_state.cleaned_data

    col = st.selectbox("Select a column to visualize", df.columns)

    if df[col].dtype in ["int64", "float64"]:
        fig, ax = plt.subplots()
        df[col].hist(bins=20, ax=ax)
        st.pyplot(fig)
    else:
        st.bar_chart(df[col].value_counts())
else:
    st.warning("Please clean the data before proceeding.")