import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="Explore Data", page_icon="🔍", layout="wide")
st.title("🔍 Explore Your Dataset")

# التحقق من توفر البيانات في session_state
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state.uploaded_file

    try:
        # قراءة الملف حسب امتداده
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("⚠️ Unsupported file format.")
            st.stop()

        st.success("✅ Dataset loaded successfully!")

        # معاينة أولية
        st.subheader("👁️ Preview:")
        st.dataframe(df.head(10))

        # خصائص البيانات
        st.subheader("📐 Basic Info:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.markdown("**Columns:**")
        st.write(list(df.columns))

        # إحصائيات رقمية
        st.subheader("📊 Summary Statistics:")
        st.write(df.describe())

        # تحليل أعمدة فردية
        st.subheader("🔎 Column Insights:")
        selected_column = st.selectbox("Select a column:", df.columns)
        if selected_column:
            st.write("🧬 Unique values:", df[selected_column].nunique())
            st.write("📋 Top frequent values:")
            st.write(df[selected_column].value_counts().head(10))

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.warning("⚠️ No dataset found. Please upload a file from the homepage.")