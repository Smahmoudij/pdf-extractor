# PDF Field Extractor

A Python tool that extracts structured data from PDF documents using the OpenAI API.

## What it does

Reads a PDF file, sends the text to an LLM, and returns a structured JSON with key fields extracted — including document type, financial metrics, time period, and risk factors.

## Motivation

Built as a prototype to explore how LLMs can automate data extraction from financial and insurance documents — a use case relevant to underwriting workflows where analysts manually process large sets of policy documents.

## Example output

```json
{
  "document_type": "insurance policy",
  "project_or_policy_name": "RBC Life Insurance Policy",
  "key_financial_metrics": null,
  "time_period": "July 1, 2025",
  "main_conclusion": "You have a right to examine this policy for 10 days.",
  "risk_factors": "This policy contains a provision removing or restricting the right of the insured to designate persons to whom or for whose benefit insurance money is to be payable."
}
```

## How it works

1. `pdfplumber` extracts raw text from the PDF
2. Text is sent to `gpt-4o-mini` with a structured prompt
3. The model returns a JSON object with the extracted fields

## Limitations discovered

- Extracting only the first 4000 characters misses financial metrics that appear later in the document — chunking strategy is a key design decision for longer documents
- Scanned PDFs (image-based) require OCR before text extraction is possible

## Setup

```bash
pip install openai pdfplumber python-dotenv
```

Add your OpenAI API key to a `.env` file: