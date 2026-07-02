import streamlit as st

from parser import extract_text
from detector import (
    detect_sensitive_data,
    detect_confidential_information,
    total_sensitive_items,
    mask_value
)
from classifier import classify_risk
from summarizer import generate_summary
from chatbot import ask_question
from report_generator import generate_report
import plotly.express as px
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import re
import cv2
import numpy as np
from rag_engine import RAGEngine
# ==========================================================
# OCR Functions
# ==========================================================

def clean_ocr_text(text):
    text = re.sub(
    r"SBINO+",
    "SBIN0",
    text
)

    replacements = {

        "EmaiI": "Email",
        "gmaiI": "gmail",
        "GmaiI": "Gmail",

        "APLKEY":"APIKEY",
        "APIKEY =":"APIKEY:",

        "EmpIoyee": "Employee",
        "Emp1oyee": "Employee",
        "EMP1O1":"EMP101",
        "EMPIOI":"EMP101",
        "EMPI0!": "EMP101",
        
        

        "TamiI": "Tamil",

        "I234": "1234",
        "I012": "1012",
        "O": "0",
        
        "gmaiI. com":"gmail.com",
        "gmaiI com":"gmail.com",
        "@ gmail":"@gmail",
        "@gmaiI":"@gmail",
        "com":"com"
    }


    for wrong, correct in replacements.items():

        text = text.replace(wrong, correct)
        text = text.replace("LinkedIn", "\nLinkedIn")


    # email spacing fix
    text = re.sub(
        r"(\w+)@(\w+)\s+(\w+)",
        r"\1@\2.\3",
        text
    )
    # Fix OCR email mistakes
    text = re.sub(
        r'([A-Za-z0-9._%+-]+)\s+gmail\.com',
        r'\1@gmail.com',
        text
    )

    text = re.sub(
        r'([A-Za-z0-9._%+-]+)\s+gmaiI\.com',
        r'\1@gmail.com',
        text
    )


    text = re.sub(r'\n\s*\n+', '\n\n', text)

    text = re.sub(r' +',' ',text)
    text = text.replace("sk_test_ ", "sk_test_")
    text = text.replace("@ ", "@")

    return text.strip()

    
def extract_text_from_image(image):

    img = np.array(image)


    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )


    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3
    )


    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    gray = cv2.medianBlur(gray, 3)

    text = pytesseract.image_to_string(
        gray,
        config="--oem 3 --psm 6"
    )


    text = clean_ocr_text(text)


    return text
def extract_text_from_scanned_pdf(uploaded_file):

    images = convert_from_bytes(
        uploaded_file.read(),
        poppler_path=r"C:\Users\Anantha Lakshmi\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )

    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Sensitive Data Detection & Compliance Assistant",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Sensitive Data Detection & Compliance Assistant")

st.markdown("""
Upload a **PDF**, **TXT**, or **CSV** document to:

- 🔍 Detect Sensitive Information
- ⚠️ Classify Risk Level
- 🤖 Generate AI Compliance Summary
- 💬 Ask Questions About the Document
- 📥 Download Security Report
""")


# ==========================================================
# File Upload
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "txt", "csv", "png", "jpg", "jpeg"]
)


# ==========================================================
# Main Application
# ==========================================================

if uploaded_file is not None:
    
    st.success(f"✅ File Uploaded Successfully : {uploaded_file.name}")

    # ------------------------------------------------------
    # Extract Text + OCR
    # ------------------------------------------------------

    file_type = uploaded_file.type

    # Extract text based on file type
    if file_type.startswith("image"):

        image = Image.open(uploaded_file)

        text = extract_text_from_image(image)

    elif file_type == "application/pdf":

        text = extract_text(uploaded_file)

        # If parser couldn't extract text, use OCR
        if text.strip() == "":
            uploaded_file.seek(0)
            text = extract_text_from_scanned_pdf(uploaded_file)

    else:

        text = extract_text(uploaded_file)


# ------------------------------------------------------
# Build RAG Index (Only Once Per Uploaded Document)
# ------------------------------------------------------

    if (
        "rag" not in st.session_state
        or st.session_state.get("current_file") != uploaded_file.name
    ):

        st.session_state.rag = RAGEngine()

        st.session_state.rag.build_index(text)

        st.session_state.current_file = uploaded_file.name
        # ------------------------------------------------------
        # Detect Sensitive Data
        # ------------------------------------------------------

    results = detect_sensitive_data(text)

    confidential = detect_confidential_information(text)

    results["Confidential Business Information"] = confidential

    # ------------------------------------------------------
    # Risk Classification
    # ------------------------------------------------------

    risk, total_score, score_details = classify_risk(results)

    # ------------------------------------------------------
    # AI Summary
    # ------------------------------------------------------

    with st.spinner("Generating AI Compliance Summary..."):

        try:
            summary = generate_summary(text)

        except Exception:

            summary = "⚠️ AI Summary unavailable."

    # ------------------------------------------------------
    # Generate Report
    # ------------------------------------------------------

    report = generate_report(
        results,
        risk,
        total_score,
        summary
    )

    # ======================================================
    # Extracted Text
    # ======================================================

    mask_data = st.checkbox(
        "🔒 Mask Sensitive Data",
        value=True
)

    display_text = text

    if mask_data:

        for category, values in results.items():

            for item in values:

                display_text = display_text.replace(
                    item,
                    mask_value(item)
                )

    st.subheader("📄 Extracted Text")

    st.text_area(
        "Document Content",
        display_text,
        height=300
)
    # ======================================================
    # Sensitive Data Detection
    # ======================================================

    st.divider()

    st.subheader("🔍 Sensitive Data Detection")

    found_any = False

    for category, values in results.items():
        
        with st.expander(category):

            if values:

                found_any = True

                for item in values:

                    if mask_data:

                        st.success(mask_value(item))

                    else:

                        st.success("🔓 " + item)
            else:

                st.info("No Data Found")

    if not found_any:
        st.success("✅ No Sensitive Information Detected.")

    # ======================================================
    # Overall Detection
    # ======================================================

    st.divider()

    total_items = total_sensitive_items(results)

    st.subheader("📊 Dashboard")
    

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Sensitive Items",
            total_items
    )

    with col2:
        st.metric(
            "Risk Score",
            total_score
        )

    with col3:
        st.metric(
            "Risk Level",
            risk
        )
    # =====================================================
    # Dashboard Charts
    # =====================================================

    chart_data = pd.DataFrame({

        "Category": list(results.keys()),

        "Count": [len(v) for v in results.values()]

    })
    st.subheader("📈 Sensitive Data Distribution")

    bar = px.bar(

        chart_data,

        x="Category",

        y="Count",

        text="Count",

        title="Sensitive Data by Category"

    )

    st.plotly_chart(bar, use_container_width=True)
    pie = px.pie(

        chart_data,

        names="Category",

        values="Count",

        title="Sensitive Data Percentage"

    )

    st.plotly_chart(pie, use_container_width=True)
    # ======================================================
    # Risk Classification
    # ======================================================

    st.divider()

    st.subheader("⚠️ Risk Classification")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Risk Level",
            risk
        )

    with col2:

        st.metric(
            "Risk Score",
            total_score
        )

    st.subheader("Risk Score Breakdown")

    risk_df = pd.DataFrame({

    "Category": list(score_details.keys()),

    "Risk Score": list(score_details.values())

})

    st.dataframe(

        risk_df,

        use_container_width=True,

        hide_index=True

    )

    # ======================================================
    # AI Summary
    # ======================================================

    st.divider()

    st.subheader("🤖 AI Compliance Summary")

    st.write(summary)

    # ======================================================
    # Ask Questions
    # ======================================================

    st.divider()

    st.subheader("💬 Ask Questions About the Document")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Get Answer"):

        if question.strip() != "":

            with st.spinner("Generating Answer..."):

                answer = ask_question(
                    st.session_state.rag,
                    question
)

            st.success(answer)

        else:

            st.warning("Please enter a question.")

    # ======================================================
    # Download Report
    # ======================================================

    st.divider()

    st.subheader("📥 Download Report")

    st.download_button(
        label="📄 Download Security Report",
        data=report,
        file_name="Sensitive_Data_Report.txt",
        mime="text/plain"
    )

else:

     st.info("👆 Please upload a PDF, TXT, CSV, or Image document to begin.")