import streamlit as st
import pandas as pd

st.set_page_config(page_title="Statistics", page_icon="📊")
st.title("📊 Statistical Analysis")

if "cleaned_data" in st.session_state:
    df = st.session_state.cleaned_data
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns

    selected_col = st.selectbox("Select a numeric column", numeric_cols)

    if selected_col:
        st.write("📈 Mean:", df[selected_col].mean())
        st.write("📉 Std:", df[selected_col].std())
        st.write("🔢 Min:", df[selected_col].min())
        st.write("🔺 Max:", df[selected_col].max())
else:
    st.warning("Please clean the data before proceeding.")