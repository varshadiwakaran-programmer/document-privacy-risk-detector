import streamlit as st
import pandas as pd

from src.privacy_risk import analyze_document, build_highlighted_text, extract_text


st.set_page_config(page_title="Smart Data Privacy Risk Detection", page_icon="🔒")
st.title("Smart Data Privacy Risk Detection for Documents")
st.caption("Upload a document to detect sensitive data and assess privacy risk.")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "txt", "docx"],
    help="Supported formats: PDF, TXT, DOCX",
)

if uploaded_file is not None:
    with st.spinner("Processing document..."):
        text = extract_text(uploaded_file)
        if not text.strip():
            st.warning("No readable text found in the uploaded file.")
            st.stop()

        result = analyze_document(text)

    st.success(f"Document processed successfully: {uploaded_file.name}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Score", result["risk_score"])
    col2.metric("Findings", result["total_findings"])
    col3.metric("Risk Level", result["risk_level"])

    with st.expander("Risk summary", expanded=True):
        st.write(
            "This document contains sensitive information patterns that may increase privacy exposure. "
            "The score is estimated using a weighted rule-based detection system."
        )

    if result["findings"]:
        findings_df = pd.DataFrame(result["findings"])
        findings_df["type"] = findings_df["type"].str.title()
        st.dataframe(findings_df[["type", "value", "score"]], use_container_width=True)

        st.subheader("Highlighted risky content")
        highlighted = build_highlighted_text(text, result["findings"])
        st.markdown(highlighted[:5000], unsafe_allow_html=True)
    else:
        st.info("No sensitive patterns were detected in this document.")

else:
    st.info("Please upload a document to begin analysis.")

st.markdown("---")
st.markdown(
    "This app is intended for educational and prototype use to detect sensitive information in documents."
)
