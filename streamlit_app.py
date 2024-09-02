import streamlit as st
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()




# Function to merge data
def merge_data(dfs, selected_headers):
    merged_data = pd.concat([df[selected_headers] for df in dfs], ignore_index=True)
    return merged_data

    # Main application
st.title("Data Merger Tool by Hues Analytics")

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
