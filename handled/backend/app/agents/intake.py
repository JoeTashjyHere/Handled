from typing import Any


def extract_receipt_fields_stub(file_path: str) -> dict[str, Any]:
    return {
        "merchant": None,
        "date": None,
        "amount": None,
        "category": None,
        "confidence": 0.0,
        "source_file": file_path,
    }
