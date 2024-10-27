import streamlit as st
import os
from io import BytesIO

# Function to read the contents of a single file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        st.error(f"Error reading file {file_path}: {e}")
        return None

# Function to merge contents of multiple RIS and ENW files, avoiding duplicates
def merge_files(uploaded_files):
    # Initialize sets to store .ris and .enw file contents
    ris_contents = set()
    enw_contents = set()

    # Process uploaded files
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        if file_name.endswith('.ris'):
            file_content = uploaded_file.read().decode('utf-8')
            ris_contents.add(file_content)
        elif file_name.endswith('.enw'):
            file_content = uploaded_file.read().decode('utf-8')
            enw_contents.add(file_content)
        else:
            st.warning(f"Skipping non-RIS/ENW file: {file_name}")

    # Merge all .ris and .enw file contents into a single string
    merged_ris_content = '\n'.join(ris_contents)
    merged_enw_content = '\n'.join(enw_contents)

    return merged_ris_content, merged_enw_content

# Streamlit app layout
st.title("Reference File Merger")
st.write("Upload .ris and .enw files to merge them into single output files without duplicates.")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload .ris and .enw files", type=['ris', 'enw'], accept_multiple_files=True)

if uploaded_files:
    # Perform merging
    merged_ris_content, merged_enw_content = merge_files(uploaded_files)

    # Save merged content to in-memory files
    merged_ris = BytesIO()
    merged_enw = BytesIO()

    merged_ris.write(merged_ris_content.encode('utf-8'))
    merged_enw.write(merged_enw_content.encode('utf-8'))

    # Prepare files for download
    merged_ris.seek(0)
    merged_enw.seek(0)

    st.download_button(
        label="Download Merged RIS File",
        data=merged_ris,
        file_name="merged_output.ris",
        mime="application/x-research-info-systems"
    )

    st.download_button(
        label="Download Merged ENW File",
        data=merged_enw,
        file_name="merged_output.enw",
        mime="application/x-endnote-refer"
    )

    st.success("Merging complete! Download your merged files.")
else:
    st.info("Please upload .ris and .enw files to start merging.")

st.info("Created by Dr. Satyajeet Patil")
st.info("For more cool apps like this visit: https://patilsatyajeet.wixsite.com/home/python")
