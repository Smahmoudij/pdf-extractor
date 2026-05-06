import pdfplumber
import os
from pathlib import Path

def get_all_files(vdr_path):
    vdr = Path(vdr_path)
    files = []
    for file in vdr.rglob("*"):
        if file.is_file() and file.suffix in [".pdf", ".docx", ".xlsx", ".txt"]:
            files.append(file)
    return files

def extract_text(file_path):
    file_path = Path(file_path)
    text = ""
    
    if file_path.suffix == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    
    elif file_path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    
    else:
        text = f"[Unsupported file type: {file_path.suffix}]"
    
    return {
        "file_path": str(file_path),
        "file_name": file_path.name,
        "folder": file_path.parent.name,
        "extension": file_path.suffix,
        "text": text,
        "char_count": len(text)
    }

if __name__ == "__main__":
    print("Scanning VDR...\n")
    
    files = get_all_files("vdr_sample")
    print(f"Found {len(files)} files:\n")
    
    documents = []
    for file in files:
        print(f"Reading: {file}")
        doc = extract_text(file)
        documents.append(doc)
        print(f"  → {doc['char_count']} characters extracted")
    
    print(f"\nDone. {len(documents)} documents ready for processing.")