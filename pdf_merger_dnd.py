import streamlit as st
from PyPDF2 import PdfMerger
import io

# -------------------
# Streamlit UI
# -------------------

st.set_page_config(page_title="📎 PDF Merger Tool", page_icon="📎", layout="centered")

st.title("📎 PDF Merger Tool")
st.write("Upload **two or more PDF files** to merge them into one.")

# File uploader
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) >= 2:
    if st.button("🔄 Merge PDFs"):
        try:
            merger = PdfMerger()
            
            # Add uploaded PDFs
            for pdf in uploaded_files:
                merger.append(pdf)
            
            # Save merged PDF to memory
            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merger.close()
            merged_pdf.seek(0)

            # Download button
            st.success("✅ PDFs merged successfully!")
            st.download_button(
                label="📥 Download Merged PDF",
                data=merged_pdf,
                file_name="merged.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    st.info("Please upload at least **two PDF files** to merge.")
