# Smart Data Privacy Risk Detection for Documents

This project detects sensitive data in uploaded documents and classifies the privacy risk level as Low, Medium, High, or Critical.

## Features
- Upload PDF, TXT, and DOCX files
- Extract document text
- Detect common sensitive data types:
  - Emails
  - Phone numbers
  - Aadhaar/ID numbers
  - PAN numbers
  - Bank account numbers
  - Names and addresses
  - Medical and financial keywords
- Compute a privacy risk score
- Show findings in a table
- View a simple summary report

## Tech stack
- Python
- Streamlit
- PyMuPDF
- python-docx
- Regex-based detection + scoring

## Installation

1. Clone the repo
2. Create a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   └── privacy_risk.py
└── .gitignore
```

## Example usage

- Upload a PDF or text document containing names, phone numbers, IDs, or account information.
- The app will identify the risky entries and categorize the document risk.

## Risk scoring

A simple weighted model is used:
- Email: +8
- Phone number: +6
- Aadhaar/ID: +18
- PAN: +15
- Bank account: +12
- Address: +10
- Medical keyword: +12
- Financial keyword: +10

The total score is mapped to:
- 0–25: Low
- 26–50: Medium
- 51–75: High
- 76+: Critical

## Scope
This project is designed as a practical academic or portfolio project for privacy, NLP, and document analysis use cases.
