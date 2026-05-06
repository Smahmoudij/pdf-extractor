from openai import OpenAI
from dotenv import load_dotenv
import os
from vdr_ingest import get_all_files, extract_text


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_document(doc):
    # Only send first 2000 characters — enough to identify document type
    preview = doc["text"][:2000]
    
    prompt = f"""You are a financial document analyst working for a reinsurance company.
Classify this document into exactly one of these categories:
- financial_report
- insurance_policy  
- legal_contract
- actuarial_report
- regulatory_filing
- other

Also extract:
- A one sentence description of what this document is about
- The company or entity it relates to
- The year or time period it covers

Document preview:
{preview}

Return ONLY a JSON object with these exact keys:
- document_type
- description
- entity
- time_period

No explanation, just JSON."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    import json
    result = json.loads(raw)
    
    # Add original file metadata to result
    result["file_name"] = doc["file_name"]
    result["folder"] = doc["folder"]
    result["file_path"] = doc["file_path"]
    result["char_count"] = doc["char_count"]
    
    return result


if __name__ == "__main__":
    import json
    
    print("Loading documents from VDR...\n")
    files = get_all_files("vdr_sample")
    
    classified = []
    for file in files:
        print(f"Reading: {file.name}")
        doc = extract_text(file)
        
        print(f"  Classifying...")
        result = classify_document(doc)
        classified.append(result)
        
        print(f"  Type: {result['document_type']}")
        print(f"  Entity: {result['entity']}")
        print(f"  Period: {result['time_period']}")
        print()
    
    # Save results to a JSON file for Layer 3 to use
    with open("classified_documents.json", "w") as f:
        json.dump(classified, f, indent=2)
    
    print(f"Done. {len(classified)} documents classified.")
    print("Results saved to classified_documents.json")