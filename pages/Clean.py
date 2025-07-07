import streamlit as st
import pandas as pd
import numpy as np # Required for np.nan if used in default data

# --- 0. Page Configuration ---
st.set_page_config(
    page_title="InsightBox - Clean Data", # Page title for the browser tab
    layout="wide",
    page_icon="🧼",
    initial_sidebar_state="expanded",
)

st.title("Clean your data 🧼")

# --- Sidebar Navigation (Assuming this is for a multi-page app structure) ---
# It's generally better to define sidebar navigation in main.py or a shared module
# to avoid duplication across pages. However, keeping it as per user's request.

st.sidebar.title("Actions")
st.sidebar.page_link("main.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/Explore.py", label="Explore Data", icon="🔍")
st.sidebar.page_link("pages/Clean.py", label="Clean Data ", icon="🧼")
st.sidebar.page_link("pages/Transform.py", label="Transform Columns", icon="🔀",disabled=True)
st.sidebar.page_link("pages/Statistical.py", label="Statistical Analysis", icon="📊", disabled=True)
st.sidebar.page_link("pages/Visualization.py", label="Data Visualization", icon="📈", disabled=True)
st.sidebar.page_link("pages/Prediction.py", label="Prediction", icon="🤖", disabled=True)
st.sidebar.page_link("pages/Report.py", label="Generate Report", icon="📄",disabled=True)

# --- 1. Initialize and Manage DataFrame in Session State ---
# This block ensures the DataFrame persists across interactions and loads from uploaded file.

# Check if a file has been uploaded in the session state (e.g., from Home page)
if "uploaded_file" in st.session_state and st.session_state.uploaded_file is not None:
    uploaded_file = st.session_state.uploaded_file

    # --- Start of fix for 'UploadedFile' object has no attribute 'id' ---
    # Create a unique identifier for the uploaded file using its name and size
    current_file_identifier = f"{uploaded_file.name}-{uploaded_file.size}"

    # Use this identifier to detect if the file has changed to avoid re-reading unnecessarily
    if 'current_loaded_file_identifier' not in st.session_state or st.session_state.current_loaded_file_identifier != current_file_identifier:
        
        uploaded_file.seek(0)  # Important: Reset file pointer to the beginning before reading
        
        try:
            # Read the file based on its extension
            if uploaded_file.name.endswith(".csv"):
                new_df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                new_df = pd.read_excel(uploaded_file)
            else:
                st.error("❌ The file format is not supported yet. The supported formats are: CSV & Excel.") # Unsupported file format
                # Reset session state for df if format is unsupported
                st.session_state.df = pd.DataFrame() 
                st.session_state.current_loaded_file_identifier = None # Clear identifier
                st.stop() # Stop execution if file format is not supported

            st.success("✅ Dataset loaded successfully.") # Dataset loaded successfully
            st.session_state.df = new_df.copy() # Store a copy of the loaded DataFrame in session_state
            st.session_state.current_loaded_file_identifier = current_file_identifier # Store the new identifier
            # st.rerun() # Uncomment if you need an immediate rerun after file upload to refresh UI
            
        except Exception as e:
            st.error(f"❌ Error reading or processing file: {e}") # Error reading or processing file
            st.session_state.df = pd.DataFrame() # Set to empty DataFrame on error
            st.session_state.current_loaded_file_identifier = None
            st.stop() # Stop execution on error
    # --- End of fix ---

# If no file is uploaded or df is not yet in session_state (e.g., first run without upload)
if 'df' not in st.session_state or st.session_state.df.empty:
    st.warning("⚠️Please upload a file from the home page first.") # Please upload a dataset
    st.stop() # Stop further execution if no DataFrame is available

# Always use the DataFrame from session_state for the rest of the app
df = st.session_state.df

# --- 2. Choose an operation ---

select_operation = st.radio("Which data you would like to handle? ",
        ["Missing data"],
        horizontal=True) 

if select_operation == "Missing data":
    # --- 3. Missing Values Summary ---
    count_of_missing = df.isnull().sum().sum()
    st.header("Handle missing data") 
    st.subheader("🕳️ Summary of missing data")
    if count_of_missing > 0:
         st.caption(f"This dataset has {count_of_missing} rows of missing values distributed as:")
    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]
    missing_df = missing_df[missing_df["Missing Values"] > 0]

    if missing_df.empty:
        st.success("🎉 No missing data found!") # No missing values detected!
    else:
        st.dataframe(missing_df)

        st.markdown("### 🛠️ How would you like to handle them?") # How would you like to handle them?

        cleaning_option = st.radio(
            "Choose a strategy:", # Choose a strategy:
            ["❌ Drop rows with missing values", # Drop rows with missing values
            "🔧 Fill columns with (mean / median / zero) value (Only for the numarical ones)", # Fill numeric columns (mean / median / zero)
            "📊 Fill columns with the most frequent value (Only for the categorical ones)",
            "✏️ Fill manually with a custom value"], # Fill manually with a custom value
            index=0,
            key="cleaning_strategy_radio_clean" # Unique key for this radio button
        )
    
        # --- 4. Column Selection Interface (Applies to all cleaning operations) ---
        st.subheader("Choose columns to apply:") # Choose columns to apply:
        col_select1, col_select2 = st.columns(2) # Use new variable names to avoid potential conflicts

        # Initialize session state for column selection
        if 'all_cols_selected_state' not in st.session_state:
            st.session_state.all_cols_selected_state = False
        if 'custom_cols_selected_list_state' not in st.session_state:
            st.session_state.custom_cols_selected_list_state = []

        # Button for "All Columns"
        if col_select1.button("All columns", key="all_cols_btn_clean"): # Unique key
            st.session_state.all_cols_selected_state = True
            st.session_state.custom_cols_selected_list_state = [] # Clear custom selection
            st.rerun() # Rerun to update UI based on new selection state

        # Multiselect for "Custom Columns"
        current_custom_selection = col_select2.multiselect(
            "or custom columns:", # Or custom columns:
            options=df.columns.tolist(),
            default=st.session_state.custom_cols_selected_list_state, # Retain previous selection
            key="custom_cols_multiselect_clean" # Unique key
        )

    # Update session state when custom multiselect changes
    if not missing_df.empty and current_custom_selection != st.session_state.custom_cols_selected_list_state:
        st.session_state.custom_cols_selected_list_state = current_custom_selection
        st.session_state.all_cols_selected_state = False # Clear "All Columns" selection
        st.rerun() # Rerun to update UI

    # ------------------------------------------------------------------

    # --- 5. Cleaning Operations Logic ---

    # --- 5.1. Drop rows with missing values ---
    if not missing_df.empty and cleaning_option == "❌ Drop rows with missing values":
        st.markdown("---")
        st.subheader("Remove rows with missing values:") # Remove rows with missing values
        commit_drop_button = st.button("Commit drop missing values", key="commit_drop_clean") # Unique key

        if commit_drop_button:
            original_rows = df.shape[0]
            
            # Logic based on stored selection state
            if st.session_state.all_cols_selected_state:
                df.dropna(inplace=True)
                removed_rows = original_rows - df.shape[0]
                st.info(f"🧹 **{removed_rows}** rows had been removed.") # Removed X rows from all columns
            elif st.session_state.custom_cols_selected_list_state:
                if not st.session_state.custom_cols_selected_list_state:
                    st.warning("Please select at least one column.") # Please select at least one column
                else:
                    df.dropna(subset=st.session_state.custom_cols_selected_list_state, inplace=True)
                    removed_rows = original_rows - df.shape[0]
                    st.info(f"🧹 **{removed_rows}** rows had been removed from the columns: **{', '.join(st.session_state.custom_cols_selected_list_state)}**.") # Removed X rows from selected columns
            else:
                st.warning("Before commit this operation, please select all columns or custom columns.") # Please choose an option
            
            st.dataframe(df) # Display DataFrame after modification

    # --- 5.2. Fill numeric columns (mean / median / zero) ---
    elif not missing_df.empty and cleaning_option == "🔧 Fill columns with (mean / median / zero) value (Only for the numarical ones)":
        st.markdown("---")
        st.subheader("Fill missing numeric values:") # Fill missing numeric values
        strategy = st.selectbox("Select the filling way:", ["Mean", "Median", "Zero"], key="fill_strategy_select_clean_numeric") # Unique key
        
        
           # --- Start of modification: Filter numeric columns to include only those with missing values ---
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
        numeric_cols_with_missing = numeric_cols[df[numeric_cols].isnull().any()].tolist()
        # --- End of modification ---
        
        commit_fill_numeric_button = st.button("تطبيق الملء الرقمي", key="commit_fill_numeric_clean") # Unique key

        if commit_fill_numeric_button:
            cols_to_fill = []
            if st.session_state.all_cols_selected_state:
                cols_to_fill = numeric_cols_with_missing # All numeric columns with missing values
            elif st.session_state.custom_cols_selected_list_state:
                # Filter custom selected columns to include only numeric ones with missing values
                cols_to_fill = [col for col in st.session_state.custom_cols_selected_list_state if col in numeric_cols_with_missing]
            
            if not cols_to_fill:
                 st.warning("الرجاء اختيار 'كل الأعمدة' أو تحديد أعمدة رقمية مخصصة تحتوي على قيم مفقودة.") # Please select 'All Columns' or specific numeric columns with missing values
            else:
                for col in cols_to_fill:
                    if col in df.columns: # Ensure column still exists (good practice)
                        # Check if the column actually has missing values before attempting to fill
                        if df[col].isnull().any():
                            if strategy == "Mean":
                                df[col].fillna(df[col].mean(), inplace=True)
                            elif strategy == "Median":
                                df[col].fillna(df[col].median(), inplace=True)
                            elif strategy == "Zero":
                                df[col].fillna(0, inplace=True)
                        else:
                            st.info(f"ℹ️ العمود '{col}' لا يحتوي على قيم مفقودة لملئها.") # Column has no missing values to fill
                
                st.success(f"✅ تم ملء القيم الرقمية المفقودة في **{', '.join(cols_to_fill)}** باستخدام `{strategy}`.") # Missing numeric values filled
                st.dataframe(df)

    # --- 5.3.  Fill the categorical columns with the most frequent value  ---
    elif not missing_df.empty and cleaning_option == "📊 Fill columns with the most frequent value (Only for the categorical ones)":
        st.markdown("---")
        st.subheader("Fill missing values:") # Fill missing values
        #strategy = st.selectbox("Select the filling way:", ["Mean", "Median", "Zero"], key="fill_strategy_select_clean_numeric") # Unique key
        
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        categorical_cols_with_missing = categorical_cols[df[categorical_cols].isnull().any()].tolist()
        
        commit_fill_categorical_button = st.button("Commit filling", key="commit_fill_categorical_clean") # Unique key

        if commit_fill_categorical_button:
            cols_to_fill = []
            if st.session_state.all_cols_selected_state:
                cols_to_fill = categorical_cols_with_missing # All categorical columns
            elif st.session_state.custom_cols_selected_list_state:
                # Filter custom selected columns to include only categorical ones
                cols_to_fill = [col for col in st.session_state.custom_cols_selected_list_state if col in categorical_cols_with_missing]
            
            if not cols_to_fill:
                 st.warning("Please select 'All Columns' or specific categorical columns.") # Please select 'All Columns' or specific numeric columns
            else:
                for col in cols_to_fill:
                    if col in df.columns: # Ensure column still exists (good practice)
                        mode_result = df[col].mode()
                        if not mode_result.empty:
                            mode_val = mode_result[0] 
                            df[col].fillna(mode_val, inplace=True)
                        else:
                           st.warning(f"⚠️ No frequent value found to fill column '{col}'. It might contain all missing values.") # No mode found
                
                st.success(f"✅ Missing values in the **{', '.join(cols_to_fill)}** columns, filled with the most frequent value.") # Missing numeric values filled
                st.dataframe(df)

                       

    # --- 5.4. Fill manually with a custom value ---
    elif not missing_df.empty and cleaning_option == "✏️ Fill manually with a custom value":
        st.markdown("---")
        st.subheader("Fill manually with a custom value:") # Fill manually with a custom value
        custom_fill_value = st.text_input("Enter a value to fill the missing values:", key="manual_fill_value_input_clean") # Unique key
        
        commit_fill_manual_button = st.button("Commit the manual filling", key="commit_fill_manual_clean") # Unique key

        if commit_fill_manual_button:
            if not custom_fill_value:
                st.warning("Please enter a value!.") # Please enter a value
            elif not st.session_state.all_cols_selected_state and not st.session_state.custom_cols_selected_list_state:
                st.warning("Please select 'All Columns' or custom columns.") # Please select 'All Columns' or custom columns
            else:
                cols_to_fill = []
                if st.session_state.all_cols_selected_state:
                    cols_to_fill = df.columns.tolist() # All columns
                elif st.session_state.custom_cols_selected_list_state:
                    cols_to_fill = st.session_state.custom_cols_selected_list_state # Selected custom columns
                
                for col in cols_to_fill:
                    if col in df.columns: # Ensure column still exists
                        df[col].fillna(custom_fill_value, inplace=True)
                
                st.success(f"✅ Missing values in the  **{', '.join(cols_to_fill)}** columns, filled with `{custom_fill_value}`.") # Missing values filled
                st.dataframe(df)

    # --- 5. Final Preview After Cleaning ---
   # st.markdown("---")
    #st.subheader("📊 معاينة بعد التنظيف:") # Preview After Cleaning
    #st.dataframe(df.head(10))


else:
    # --- 7. Duplicated values ---
    count_of_duplicated = df.duplicated().sum()
    
    if count_of_duplicated < 1:
        st.success("🎉 No duplicated data found!") # No duplicated values detected!
    else:
     
        st.header(" Handle duplicated data")     
        st.subheader("♻️ Summary of duplicated data")

        st.caption("This is based on all the rows, if you want to customize ")

        col1,col2 = st.columns(2)
        all_rows = col1.button("All rows")
        custome_rows = col2.multiselect("Custome rows",df.columns.tolist())

        st.caption(f"This dataset has {count_of_duplicated} rows of duplicated values distributed as:")
        if all_rows:
            duplicated_df = df[df.duplicated]
            duplicated_df
        elif custome_rows:

             duplicated_df = df[df.duplicated(subset=custome_rows)]
             duplicated_df

        #st.dataframe(duplicated_df)
        
        

        
       

        st.markdown("### 🛠️ How would you like to handle them?") # How would you like to handle them?


# --- 6. Save Cleaned Data to Session State ---
st.markdown("---")
save_changes = st.button("💾 Save you changes?", key="save_changes_clean")
st.caption("if you wolud like to go ahead through other sections")
if save_changes: # Unique key
    st.session_state.cleaned_data = df.copy() # Save a copy of the modified DataFrame
    st.info("Your changes have been saved!") # Your changes have been saved!
    st.dataframe(st.session_state.cleaned_data.head()) # Display for confirmation

#to_download = convert_for_download(df)
st.download_button(label = "⬇️ Download your modified data (as .csv)", data= df.to_csv(), file_name="modified_data.csv")

