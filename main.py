import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="InsightBox",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded", 
)
st.title("InsightBox 📊")
st.caption("Your smart journey from raw files to ready insights")
st.markdown("""
A flexible platform for data analysis, designed to simplify your exploration from raw data to meaningful analytics.  
InsightBox empowers you to explore, clean, transform, and generate predictive insights — all through an intuitive interface.  
""")
st.link_button("Develpoed by: Morad Moqbel", "https://linkedin.com/in/moradmoqbel")

st.sidebar.title("Actions")
st.sidebar.page_link("main.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/Explore.py", label="Explore Data", icon="🔍")
st.sidebar.page_link("pages/Clean.py", label="Clean Data ", icon="🧼")
st.sidebar.page_link("pages/Transform.py", label="Transform Columns", icon="🔀",disabled=True)
st.sidebar.page_link("pages/Statistical.py", label="Statistical Analysis", icon="📊", disabled=True)
st.sidebar.page_link("pages/Visualization.py", label="Data Visualization", icon="📈", disabled=True)
st.sidebar.page_link("pages/Prediction.py", label="Prediction", icon="🤖", disabled=True)
st.sidebar.page_link("pages/Report.py", label="Generate Report", icon="📄",disabled=True)
st.info("This app under development. The available pages are: Explore and clean")

st.header("Upload your file 📁 ")
st.caption("Kindly notice that in the meaning time, this tool accpets only .csv & .xlsx formats!")
data = st.file_uploader("Upload your dataset", type=["csv","xlsx"])

if data:
    if data.name.endswith(".csv"):
        df = pd.read_csv(data)
    else:
        df = pd.read_excel(data)

    st.info("Looks like you've uploaded a file! If it's the right one, feel free to explore the next step from the sidebar — or re-upload if you'd like to start over", icon="ℹ️")
    st.dataframe(df.head())
    st.session_state.uploaded_file = data

st.divider()

st.header("📘 What can you do with InsightBox?")

st.subheader("Explore Data 🔍")
st.write("Get a quick overview of your dataset — view its structure, columns, and missing values to understand your data at a glance.")
st.divider()

st.subheader("Clean Data 🧼")
st.write("Handle missing values, remove duplicates, and prepare your dataset for deeper analysis — all with easy, guided options.")
st.divider()

st.subheader("Transform Columns 🔀")
st.write("Convert data types, encode text values, or engineer new variables to reshape your dataset into analysis-ready form. ")
st.divider()

st.subheader("Statistical Analysis 📊")
st.write("Generate quick statistical summaries like mean, median, range, and standard deviation to better understand numeric patterns in your data.")
st.divider()

st.subheader("Data Visualization 📈")
st.write("Create interactive visualizations like histograms and bar charts to explore trends and distributions visually")
st.divider()

st.subheader("Prediction 🤖")
st.write("(Coming soon) Apply smart models to make predictions from your data and discover hidden insights automatically. ")
st.divider()

st.subheader("Generate Report 📄")
st.write("Export your cleaned or transformed data as a downloadable report — ready for sharing or further processing.")
st.divider()
