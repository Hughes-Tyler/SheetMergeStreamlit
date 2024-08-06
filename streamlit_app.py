import streamlit as st
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
USERNAME = os.getenv("MY_APP_USERNAME")
PASSWORD = os.getenv("MY_APP_PASSWORD")

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Function to merge data
def merge_data(dfs, selected_headers):
    merged_data = pd.concat([df[selected_headers] for df in dfs], ignore_index=True)
    return merged_data

# Function for login
def login(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
    else:
        st.error("Incorrect username or password")

# Login form
if not st.session_state.authenticated:
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")
        if submit_button:
            login(username, password)
else:
    # Main application
    st.title("Data Merger")

    # File upload
    uploaded_files = st.file_uploader("Upload your Excel files", accept_multiple_files=True, type=["xlsx"])
    if uploaded_files:
        dfs = [pd.read_excel(file) for file in uploaded_files]
        
        # Display common headers
        common_headers = list(set(dfs[0].columns).intersection(*[df.columns for df in dfs[1:]]))
        selected_headers = st.multiselect("Select headers to merge", common_headers)
        
        if st.button("Merge Data"):
            if selected_headers:
                merged_df = merge_data(dfs, selected_headers)
                st.write("Merged Data", merged_df)
                
                # Provide download link
                towrite = BytesIO()
                merged_df.to_excel(towrite, index=False, header=True)
                towrite.seek(0)
                st.download_button(
                    label="Download Merged Data",
                    data=towrite,
                    file_name='merged_data.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            else:
                st.warning("Please select headers to merge")
