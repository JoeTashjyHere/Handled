import re
from dataclasses import dataclass
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image
import pytesseract


@dataclass(frozen=True)
class OcrResult:
    text: str
    average_confidence: float


def run_ocr(image: Image.Image) -> OcrResult:
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    words = [word for word in data.get("text", []) if word.strip()]
    confidences = [int(conf) for conf in data.get("conf", []) if conf.isdigit()]
    text = " ".join(words)
    average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    return OcrResult(text=text, average_confidence=average_confidence)


def extract_structured_fields(text: str) -> dict[str, dict[str, str | float]]:
    patterns = {
        "name": r"(?:name|full name)[:\s]+(?P<value>[A-Za-z ,.'-]{2,})",
        "email": r"(?P<value>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        "phone": r"(?P<value>\+?\d[\d\s().-]{7,}\d)",
        "amount": r"(?:\$|usd)\s*(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        "date": r"(?P<value>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        "address": r"(?:address)[:\s]+(?P<value>[^\n]{5,})"
    }

    fields: dict[str, dict[str, str | float]] = {}
    for field_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            fields[field_name] = {
                "value": match.group("value").strip()
            }

    return fields


def process_intake_upload(file_path: str, confidence_threshold: float = 80.0) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ocr_results: list[OcrResult] = []

    if path.suffix.lower() == ".pdf":
        images = convert_from_path(str(path))
        for image in images:
            ocr_results.append(run_ocr(image))
    else:
        image = Image.open(path)
        ocr_results.append(run_ocr(image))

    full_text = "\n".join(result.text for result in ocr_results if result.text)
    confidences = [result.average_confidence for result in ocr_results]
    average_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    fields = extract_structured_fields(full_text)
    low_confidence = average_confidence < confidence_threshold

    return {
        "fields": fields,
        "raw_text": full_text,
        "average_confidence": round(average_confidence, 2),
        "low_confidence": low_confidence
    }
