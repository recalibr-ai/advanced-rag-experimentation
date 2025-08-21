#!/usr/bin/env python3

import sys
import os
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

def extract_text_from_pdf(pdf_path, output_path=None):
    """
    Extract text from a PDF file and save to a text file.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Optional path for output text file. If not provided,
                    will use the same name as PDF with .txt extension
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    if output_path is None:
        output_path = pdf_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            total_pages = len(pdf_reader.pages)
            print(f"Processing {pdf_path.name} ({total_pages} pages)...")
            
            all_text = []
            
            for page_num in range(total_pages):
                if page_num % 10 == 0:
                    print(f"  Processing page {page_num + 1}/{total_pages}...")
                
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if text:
                    all_text.append(f"--- Page {page_num + 1} ---\n")
                    all_text.append(text)
                    all_text.append("\n\n")
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(''.join(all_text))
            
            print(f"✓ Text extracted to: {output_path}")
            print(f"  File size: {output_path.stat().st_size:,} bytes")
            return True
            
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return False

def main():
    pdf_files = [
        "late_interaction.pdf",
        "multiple_representations.pdf", 
        "reasoning_retrievers.pdf"
    ]
    
    print("PDF Text Extraction Tool")
    print("=" * 40)
    
    success_count = 0
    
    for pdf_file in pdf_files:
        if extract_text_from_pdf(pdf_file):
            success_count += 1
        print()
    
    print("=" * 40)
    print(f"Extraction complete: {success_count}/{len(pdf_files)} files processed successfully")

if __name__ == "__main__":
    main()