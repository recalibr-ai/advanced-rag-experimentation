import PyPDF2
import sys

def split_pdf(input_file, page_ranges):
    """
    Split a PDF into multiple files based on page ranges.
    
    Args:
        input_file: Path to the input PDF file
        page_ranges: List of tuples (start_page, end_page, output_filename)
    """
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        print(f"Total pages in PDF: {total_pages}")
        
        for start_page, end_page, output_name in page_ranges:
            pdf_writer = PyPDF2.PdfWriter()
            
            # PyPDF2 uses 0-based indexing, so subtract 1 from page numbers
            for page_num in range(start_page - 1, end_page):
                if page_num < total_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    print(f"Warning: Page {page_num + 1} exceeds total pages")
            
            with open(output_name, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"Created {output_name} with pages {start_page}-{end_page}")

if __name__ == "__main__":
    input_pdf = "Beyond-Naive-RAG--Practical-Advanced-Methods (1).pdf"
    
    # Define the page ranges and output filenames
    ranges = [
        (62, 89, "reasoning_retrievers.pdf"),
        (90, 117, "late_interaction.pdf"),
        (118, 141, "multiple_representations.pdf")
    ]
    
    try:
        split_pdf(input_pdf, ranges)
        print("\nPDF split successfully!")
    except Exception as e:
        print(f"Error: {e}")