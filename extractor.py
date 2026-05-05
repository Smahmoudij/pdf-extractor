import pdfplumber
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_fields_with_llm(text):
    prompt = f"""You are a financial document analyst. 
Extract the following fields from the document text below.
Return ONLY a valid JSON object with these exact keys.
If a field is not found, use null.

Fields to extract:
- document_type
- project_or_policy_name
- key_financial_metrics
- time_period
- main_conclusion
- risk_factors

Document text:
{text[:4000]}

Return only JSON, no explanation."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)

def process_pdf(pdf_path):
    print(f"\nProcessing: {pdf_path}")
    print("-" * 50)
    
    print("Step 1: Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters of text")
    
    print("Step 2: Sending to OpenAI for field extraction...")
    fields = extract_fields_with_llm(text)
    
    print("\nExtracted fields:")
    print(json.dumps(fields, indent=2))
    
    return fields

if __name__ == "__main__":
    pdf_path = "CMQ100.pdf"
    process_pdf(pdf_path)