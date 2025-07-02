import streamlit as st

st.set_page_config(page_title="Report Generator", page_icon="📄")
st.title("📄 Generate Report")

if "cleaned_data" in st.session_state:
    df = st.session_state.cleaned_data

    if st.button("Download Cleaned Data as CSV"):
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="cleaned_data.csv")
else:
    st.warning("Please clean the data before generating a report.")