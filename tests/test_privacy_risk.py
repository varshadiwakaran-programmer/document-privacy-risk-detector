from src.privacy_risk import analyze_document, build_highlighted_text


def test_analyze_document_detects_sensitive_data():
    text = """Name: Aisha Khan
Email: aisha.khan@gmail.com
Phone: +91 98765 43210
PAN: ABCDE1234F
Address: 42 Green Park, Bengaluru
Diagnosis: Diabetes mellitus
"""
    result = analyze_document(text)
    assert result["risk_level"] in {"High", "Critical"}
    assert result["total_findings"] > 0
    assert any(f["type"] == "email" for f in result["findings"])


def test_highlighted_text_includes_markers():
    text = "Contact: rahul@example.com"
    result = build_highlighted_text(text, [{"type": "email", "value": "rahul@example.com", "score": 10}])
    assert "<mark>rahul@example.com</mark>" in result
