# 🔒 AI-Based Sensitive Data Detection & Compliance Assistant

An AI-powered document security application that detects sensitive information, classifies document risk, generates compliance summaries, and answers document-related questions using Retrieval-Augmented Generation (RAG).

---

# 📌 Project Overview

Organizations frequently handle confidential documents containing personally identifiable information (PII), financial details, passwords, API keys, and other sensitive business data.

This project automatically analyzes uploaded documents and helps users identify sensitive information, understand compliance risks, and securely review document content through an interactive dashboard.

The application supports multiple document formats, performs OCR for scanned documents, masks sensitive information, generates AI-powered compliance summaries, and provides intelligent document question answering using RAG.

---

# 🚀 Features

## 📂 Document Upload

- PDF Documents
- TXT Files
- CSV Files
- PNG Images
- JPG/JPEG Images

---

## 🔍 Sensitive Data Detection

The application detects:

- Email Addresses
- Phone Numbers
- Aadhaar Numbers
- PAN Numbers
- Employee IDs
- Bank Account Numbers
- IFSC Codes
- API Keys
- Passwords
- Credit Card Numbers
- Confidential Business Information

---

## 🔒 Data Masking

Sensitive information can be automatically masked before displaying the extracted text.

Example:

Email:
```
john@gmail.com
```

becomes

```
j*******@gmail.com
```

---

## 📄 OCR Support

Supports scanned documents using:

- Tesseract OCR
- OpenCV Image Preprocessing
- PDF to Image Conversion (Poppler)

This allows text extraction even from scanned PDFs and images.

---

## ⚠️ Risk Classification

Each document is assigned a security risk level.

Risk Levels:

- 🟢 LOW
- 🟡 MEDIUM
- 🔴 HIGH

Risk score is calculated based on detected sensitive information.

---

## 📊 Interactive Dashboard

Dashboard includes:

- Total Sensitive Items
- Risk Score
- Risk Level
- Sensitive Data Distribution (Bar Chart)
- Sensitive Data Percentage (Pie Chart)

---

## 🤖 AI Compliance Summary

Using Groq LLM, the application generates:

- Document Summary
- Sensitive Information Found
- Compliance Risks
- Security Risks
- Recommended Actions

---

## 💬 AI Document Chatbot (RAG)

Users can ask natural language questions about the uploaded document.

Example:

- What technical skills are mentioned?
- How many API keys are present?
- Does this document contain confidential information?
- Summarize the internship experience.

The chatbot answers only using information from the uploaded document.

---

## 📥 Report Generation

Generates a downloadable security report containing:

- Sensitive Data Summary
- Risk Classification
- AI Compliance Summary

---

# 🛠️ Technologies Used

## Frontend

- Streamlit

## Backend

- Python

## AI

- Groq LLM
- Retrieval-Augmented Generation (RAG)

## OCR

- Tesseract OCR
- OpenCV
- pdf2image
- Pillow

## Visualization

- Plotly
- Pandas

## Text Processing

- Regular Expressions (Regex)

---

# 🏗️ Project Architecture

```
                Upload Document
                        │
                        ▼
              Text Extraction Module
          (PDF / TXT / CSV / OCR)
                        │
                        ▼
         Sensitive Data Detection Engine
                        │
                        ▼
            Risk Classification Module
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
 AI Compliance Summary          RAG Chatbot
          │                           │
          └─────────────┬─────────────┘
                        ▼
               Interactive Dashboard
                        │
                        ▼
               Download Security Report
```

---

# 📂 Project Structure

```
SensitiveDataDetector/

│── app.py
│── parser.py
│── detector.py
│── classifier.py
│── summarizer.py
│── chatbot.py
│── rag_engine.py
│── report_generator.py
│── requirements.txt
│── README.md
│── .gitignore
│── sample_files/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/SensitiveDataDetector.git
```

Move into project directory

```bash
cd SensitiveDataDetector
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```
GROQ_API_KEY=your_api_key_here
```

---

# 📷 Sample Output

The application provides:

- Extracted Document Text
- Sensitive Information Detection
- Risk Dashboard
- AI Compliance Summary
- AI Document Chatbot
- Downloadable Security Report

---

# 🎯 Use Cases

- Enterprise Document Security
- Compliance Auditing
- HR Document Screening
- Financial Document Review
- Healthcare Record Protection
- Government Record Analysis
- Data Privacy Compliance

---

# 🔮 Future Enhancements

- FAISS Vector Database
- SQLite Audit Logging
- User Authentication
- Multi-user Support
- PDF Report Generation
- Docker Deployment
- Cloud Deployment
- Admin Dashboard
- Compliance Score Meter
- Dark Mode
- Role-Based Access Control

---

# 👩‍💻 Developer

**Hamsavarthiny P**

Aspiring Software & Full Stack Developer

GitHub:
https://github.com/Hamsa1016

LinkedIn:
https://linkedin.com/in/hamsavarthiny

---

# 📄 License

This project is developed for educational, research, and demonstration purposes.

---

# ⭐ Acknowledgements

- Streamlit
- Groq
- Plotly
- OpenCV
- Tesseract OCR
- Pillow
- Pandas