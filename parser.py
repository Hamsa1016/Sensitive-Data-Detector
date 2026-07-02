import pdfplumber
import pandas as pd

def extract_text(uploaded_file):
    """
    Extract text from PDF, TXT, or CSV file.
    """

    file_name = uploaded_file.name.lower()

    # ---------------- PDF ----------------
    if file_name.endswith(".pdf"):
        text = ""

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    # ---------------- TXT ----------------
    elif file_name.endswith(".txt"):

        text = uploaded_file.read().decode("utf-8")

        return text

    # ---------------- CSV ----------------
    elif file_name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        text = df.to_string(index=False)

        return text

    else:
        return ""