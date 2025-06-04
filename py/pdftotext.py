import fitz
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"[ERROR] Failed to extract text from {pdf_path}: {e}")
        return None
    return text

def main():
    input_dir = Path("training/texts")
    
    file = open("training/tmp/docs.txt", "w")
    file.close()
    output_file = Path("training/tmp/docs.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    with output_file.open("w", encoding="utf-8") as out:
        if not pdf_files:
            out.write("[INFO] No PDF files found.\n")
        for pdf_file in pdf_files:
            text = extract_text_from_pdf(pdf_file)
            if text:
                out.write(f"\n--- Extracted from {pdf_file.name} ---\n{text}\n")

if __name__ == "__main__":
    main()
