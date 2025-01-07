import streamlit as st
from io import BytesIO
import qrcode
import base64

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
    ris_contents = set()
    enw_contents = set()

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_content = uploaded_file.read().decode('utf-8')
        if file_name.endswith('.ris'):
            ris_contents.add(file_content)  # Preserve original content
        elif file_name.endswith('.enw'):
            enw_contents.add(file_content)  # Preserve original content
        else:
            st.warning(f"Skipping non-RIS/ENW file: {file_name}")

    # Join contents exactly as they were in the input
    merged_ris_content = ''.join(ris_contents)
    merged_enw_content = ''.join(enw_contents)

    return merged_ris_content, merged_enw_content

# Streamlit app layout
st.title("Reference File Merger")
st.write("Upload .ris and .enw files to merge them into single output files without duplicates.")

# Expandable container with custom styling
with st.expander("ℹ️ Click here to learn about this app", expanded=False):
    st.markdown("""
        This app allows you to upload multiple `.ris` and `.enw` files and merge them into single output files, avoiding duplicates.
        - **Supported Formats**: RIS (.ris) and EndNote (.enw) files.
        - **Output Files**: You can download merged RIS and ENW files.
        - **Preservation**: The original case and formatting of the data are preserved for compatibility with reference management tools like EndNote.
    """)

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload .ris and .enw files", type=['ris', 'enw'], accept_multiple_files=True)

if uploaded_files:
    merged_ris_content, merged_enw_content = merge_files(uploaded_files)

    # Save merged contents to in-memory files
    merged_ris = BytesIO()
    merged_enw = BytesIO()

    merged_ris.write(merged_ris_content.encode('utf-8'))
    merged_enw.write(merged_enw_content.encode('utf-8'))

    merged_ris.seek(0)
    merged_enw.seek(0)

    # Provide download buttons for the merged files
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

# Support section in expander
with st.expander("🤝 Support Our Research", expanded=False):
    st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin: 1rem 0;'>
            <h3>🙏 Your Support Makes a Difference!</h3>
            <p>Your contribution helps us continue developing free tools for the research community.</p>
            <p>Every donation, no matter how small, fuels our research journey!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Two columns for QR code and Buy Me a Coffee button
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### UPI Payment")
        # Generate UPI QR code
        upi_url = "upi://pay?pa=satyajeet1396@oksbi&pn=Satyajeet Patil&cu=INR"
        qr = qrcode.make(upi_url)
        
        # Save QR code to BytesIO
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Display QR code with message
        st.markdown("Scan to pay: **satyajeet1396@oksbi**")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{qr_base64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("#### Buy Me a Coffee")
        st.markdown("Support through Buy Me a Coffee platform:")
        # Buy Me a Coffee button
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
                    <img src="https://img.buymeacoffee.com/button-api/?text=Support our Research&emoji=&slug=researcher13&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Support our Research"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.info("A small donation from you can fuel our research journey, turning ideas into breakthroughs that can change lives!")
