import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transform Columns", page_icon="🔀")
st.title("🔀 Transform Columns")

if "cleaned_data" in st.session_state:
    df = st.session_state.cleaned_data.copy()
    st.dataframe(df.head())

    selected_col = st.selectbox("Select column to transform", df.columns)

    if df[selected_col].dtype == "object":
        if st.button("Convert to category (Label Encoding)"):
            df[selected_col] = df[selected_col].astype("category").cat.codes
            st.success("Column encoded.")
    elif df[selected_col].dtype in ["int64", "float64"]:
        if st.button("Convert to string"):
            df[selected_col] = df[selected_col].astype(str)
            st.success("Column converted.")

    st.session_state.transformed_data = df
else:
    st.warning("Please clean the data before proceeding.")