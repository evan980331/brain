import os
import shutil
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_path, output_dir):
    filename = os.path.basename(pdf_path)
    output_filename = filename.replace(".pdf", ".md")
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Extracting PDF: {pdf_path}...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to {output_path}")
    return output_path

def extract_text_from_docx(docx_path, output_dir):
    filename = os.path.basename(docx_path)
    output_filename = filename.replace(".docx", ".md")
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Extracting DOCX: {docx_path}...")
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to {output_path}")
    return output_path

if __name__ == "__main__":
    input_dir = "raw-sources/input"
    temp_dir = "raw-sources/temp"
    md_dir = "raw-sources/md"
    
    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        try:
            if filename.endswith(".pdf"):
                extract_text_from_pdf(file_path, md_dir)
                shutil.move(file_path, os.path.join(temp_dir, filename))
                print(f"Moved {filename} to {temp_dir}")
            elif filename.endswith(".docx"):
                extract_text_from_docx(file_path, md_dir)
                shutil.move(file_path, os.path.join(temp_dir, filename))
                print(f"Moved {filename} to {temp_dir}")
            else:
                print(f"Skipping unsupported file: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


