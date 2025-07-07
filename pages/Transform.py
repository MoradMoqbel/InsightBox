import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="InsightBox",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded", 
)
st.title("Transform your data 🔀")

st.sidebar.title("Actions")
st.sidebar.page_link("main.py", label="Home", icon="🔍")
st.sidebar.page_link("pages/Explore.py", label="Explore Data", icon="🔍")
st.sidebar.page_link("pages/Clean.py", label="Clean Data ", icon="🧼")
st.sidebar.page_link("pages/Transform.py", label="Transform Columns", icon="🔀")
st.sidebar.page_link("pages/Statistical.py", label="Statistical Analysis", icon="📊")
st.sidebar.page_link("pages/Visualization.py", label="Data Visualization", icon="📈")
st.sidebar.page_link("pages/Prediction.py", label="Prediction", icon="🤖", disabled=True)
st.sidebar.page_link("pages/Report.py", label="Generate Report", icon="📄")

# التحقق من تحميل البيانات
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state.uploaded_file
    uploaded_file.seek(0)  # تأكد من إعادة المؤشر لبداية الملف

    try:
        # قراءة البيانات حسب نوع الملف
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("⚠️ Unsupported file format.")
            st.stop()

        st.success("✅ Dataset loaded successfully")

        # 👁️ المعاينة
        st.subheader("👁️ Preview of Data")
        st.dataframe(df.head(10))