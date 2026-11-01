from __future__ import annotations

import re
from typing import List, Dict, Any


SENSITIVE_PATTERNS = [
    {
        "type": "email",
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "weight": 8,
    },
    {
        "type": "phone",
        "pattern": r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)\d{3}[-.\s]?\d{4}",
        "weight": 6,
    },
    {
        "type": "aadhaar",
        "pattern": r"\b\d{12}\b",
        "weight": 18,
    },
    {
        "type": "pan",
        "pattern": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "weight": 15,
    },
    {
        "type": "bank_account",
        "pattern": r"\b\d{9,18}\b",
        "weight": 12,
    },
    {
        "type": "ifsc",
        "pattern": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        "weight": 7,
    },
    {
        "type": "address",
        "pattern": r"\b\d{1,6}\s+[A-Za-z0-9 .,#-]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Town|City|District|State|Zip|PIN|Pincode)\b",
        "weight": 10,
    },
    {
        "type": "name",
        "pattern": r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b",
        "weight": 5,
    },
]

CONTEXT_KEYWORDS = {
    "health": ["diagnosis", "patient", "medical", "hospital", "prescription", "blood group", "treatment"],
    "financial": ["salary", "tax", "invoice", "loan", "insurance", "bank", "account", "credit card", "debit card"],
    "identity": ["passport", "aadhaar", "pan", "passport number", "national id", "identity number"],
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_text_from_pdf(file_obj) -> str:
    import fitz

    doc = fitz.open(stream=file_obj.read(), filetype="pdf")
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    return "\n".join(text_parts)


def extract_text_from_txt(file_obj) -> str:
    return file_obj.read().decode("utf-8", errors="ignore")


def extract_text_from_docx(file_obj) -> str:
    from docx import Document
    import io

    document = Document(io.BytesIO(file_obj.read()))
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text(file_obj) -> str:
    name = (file_obj.name or "").lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_obj)
    if name.endswith(".docx"):
        return extract_text_from_docx(file_obj)
    if name.endswith(".txt"):
        return extract_text_from_txt(file_obj)

    return ""


def collect_matches(text: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    normalized = normalize_text(text)

    for rule in SENSITIVE_PATTERNS:
        matches = re.findall(rule["pattern"], normalized, flags=re.IGNORECASE)
        unique_matches = sorted(set(match.strip() for match in matches if match and str(match).strip()))
        for value in unique_matches:
            findings.append(
                {
                    "type": rule["type"],
                    "value": value,
                    "score": rule["weight"],
                }
            )

    return findings


def calculate_context_boost(text: str) -> int:
    lower = text.lower()
    boost = 0
    for category, keywords in CONTEXT_KEYWORDS.items():
        if any(keyword.lower() in lower for keyword in keywords):
            boost += 12
    return boost


def map_score_to_label(score: int) -> str:
    if score <= 25:
        return "Low"
    if score <= 50:
        return "Medium"
    if score <= 75:
        return "High"
    return "Critical"


def analyze_document(text: str) -> Dict[str, Any]:
    findings = collect_matches(text)
    risk_score = sum(item["score"] for item in findings) + calculate_context_boost(text)
    risk_score = min(risk_score, 100)

    summary = {
        "total_findings": len(findings),
        "risk_score": risk_score,
        "risk_level": map_score_to_label(risk_score),
        "findings": findings,
    }

    return summary


def build_highlighted_text(text: str, findings: List[Dict[str, Any]]) -> str:
    highlighted = text
    replacements = []
    for item in findings:
        value = item["value"]
        if not value:
            continue
        escaped = re.escape(value)
        replacements.append((re.compile(escaped, flags=re.IGNORECASE), f"<mark>{value}</mark>"))

    for pattern, replacement in replacements:
        highlighted = pattern.sub(replacement, highlighted)
    return highlighted
