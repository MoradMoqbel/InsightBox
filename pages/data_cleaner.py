import streamlit as st
import pandas as pd

st.set_page_config(page_title="Clean Data", page_icon="🧼", layout="wide")
st.title("🧼 Clean Your Dataset")

# التحقق من تحميل البيانات
if "uploaded_file" in st.session_state:
    uploaded_file = st.session_state.uploaded_file

    try:
        # قراءة الملف
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("✅ Dataset loaded for cleaning")

        # عرض ملخص القيم الفارغة
        st.subheader("🕳️ Missing Values")
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0])

        # خيارات التنظيف
        st.subheader("⚙️ Cleaning Options")

        # حذف الصفوف التي تحتوي على قيم مفقودة
        if st.checkbox("🗑️ Remove rows with missing values"):
            df.dropna(inplace=True)
            st.info("✅ Rows with missing values removed")

        # تعبئة القيم المفقودة في أعمدة رقمية
        numeric_cols = df.select_dtypes(include=["float", "int"]).columns
        if numeric_cols.any():
            fill_option = st.selectbox("🔧 Fill missing numeric values with:", ["Mean", "Median", "Zero"])
            if fill_option == "Mean":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            elif fill_option == "Median":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            elif fill_option == "Zero":
                df[numeric_cols] = df[numeric_cols].fillna(0)
            st.success("✅ Missing numeric values filled")

        # حذف التكرارات
        if st.checkbox("♻️ Remove duplicated rows"):
            df.drop_duplicates(inplace=True)
            st.info("✅ Duplicate rows removed")

        # عرض النتيجة
        st.subheader("📊 Cleaned Dataset Preview")
        st.dataframe(df.head(10))

        # حفظ البيانات في session_state لاستخدامها لاحقًا
        st.session_state.cleaned_data = df

    except Exception as e:
        st.error(f"❌ Error reading the file: {e}")

else:
    st.warning("⚠️ No dataset found. Please upload it from the Home page.")