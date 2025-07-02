import streamlit as st

st.set_page_config(page_title="InsightBox", page_icon="📊")
st.title("📊 InsightBox")

st.markdown("""
**InsightBox — Your smart journey from raw files to ready insights**  
A flexible platform for data analysis, designed to simplify your exploration from messy spreadsheets to meaningful analytics.  
InsightBox empowers you to explore, clean, transform, and generate predictive insights — all through an intuitive interface.  
**Developed by Morad Moqbel**
""")

st.sidebar.title("🔧 InsightBox Menu")
uploaded_file = st.sidebar.file_uploader("📁 Upload your dataset", type=["csv", "xlsx"])

selected_operations = st.sidebar.multiselect(
    "⚙️ Select operations to perform:",
    ["Explore Data", "Clean Data", "Transform Columns",
     "Statistical Analysis", "Visualize", "Predict Values", "Generate Report"],
    default=["Explore Data"]
)

if st.sidebar.button("🚀 Run Operations"):
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.selected_operations = selected_operations
        st.sidebar.success("✅ File and operations saved")
        st.sidebar.info("Go to the corresponding page from the sidebar to begin 👈")
    else:
        st.sidebar.error("Please upload a file to proceed.")