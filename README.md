# PDF-JSON Parser
Automated Intelligent Extraction of Text and Figures from Complex PDF Textbooks.

A high-performance, AI-driven pipeline to convert complex PDF textbooks into structured JSON. Uses Unstructured.io, Poppler, and Tesseract OCR to intelligently extract text, diagrams, and figures . Perfect for building searchable digital libraries and interactive learning systems.

# Features
 Unified Extraction: Simultaneously generates clean JSON content and crops images (figures) from PDFs.
 
 Layout Awareness: Uses unstructured's high-resolution strategy to preserve the order of titles, list items, and narrative text.
 
 Automated Asset Linking: Automatically injects <img> tags into your JSON, pointing to extracted local assets.
 # Prerequisites & Dependencies
This project requires specific system-level tools to handle image processing and OCR.

# 1. Poppler (PDF Rendering)
Poppler is required for the library to understand PDF structure and page layouts.

Windows: Download the latest binaries from "https://github.com/oschwartz10612/poppler-windows/releases"(I have already uploaded the poppler file so that you can download the zip) 
# 1. Setup Poppler
Download the latest Poppler binary (e.g., Release-xx.xx.0-0.zip) from the Poppler for Windows GitHub.

Extract the zip folder to a permanent location, such as C:\Program Files\poppler.

Open the bin folder inside the extracted directory (e.g., C:\Program Files\poppler\Library\bin).

# Add to PATH:

Press the Windows Key and type "env".

Select "Edit the system environment variables".

Click the "Environment Variables" button.

Under "System variables", find Path, select it, and click "Edit".

Click "New" and paste the full path to the bin folder.

Click OK to save all windows.

Verification: Run pdftoppm -v in your terminal.

# 2. Tesseract OCR
Required for extracting text from scanned images and complex PDF diagrams.

Windows: Download the installer from "https://github.com/UB-Mannheim/tesseract/wiki".

# Setup: Install 

2. Setup Tesseract OCR

Download the Tesseract installer from the UB-Mannheim Tesseract Wiki.

Run the installer. By default, it will install to C:\Program Files\Tesseract-OCR.

# Add to PATH:

Repeat the steps above to open the "Environment Variables" window.

Under "System variables", find Path and click "Edit".

Click "New" and paste the path to your Tesseract installation folder (C:\Program Files\Tesseract-OCR).

Click OK to save.

Verification: Run tesseract --version in your terminal.



# ultimate_batch_parser.py


import os

import json

import logging

from unstructured.partition.pdf import partition_pdf

PROCESSING_MANIFEST = {

    "source_directory_1": "output_directory_1",
    
    
    "source_directory_2": "output_directory_2",
    
    
    "source_directory_3": "output_directory_3"
}

IMAGE_OUTPUT_DIR = "assets/images"

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def run_parser():
    print(f"🚀 Starting batch extraction...")
    
    for source_dir, output_dir in PROCESSING_MANIFEST.items():
        if not os.path.exists(source_dir):
            print(f"  [!] Skipping {source_dir}: Folder not found.")
            continue
            
        print(f"\n📂 Processing: {source_dir} -> {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
        
        for file in os.listdir(source_dir):
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(source_dir, file)
                json_path = os.path.join(output_dir, file.replace('.pdf', '.json'))
                
                print(f"  -> Parsing: {file}")
                
                try:
                    elements = partition_pdf(
                        filename=pdf_path,
                        strategy="hi_res",
                        extract_image_block_types=["Image"],
                        extract_image_block_output_dir=IMAGE_OUTPUT_DIR
                    )
                    
                    content = ""
                    for el in elements:
                        if "Image" in str(type(el)):
                            if hasattr(el.metadata, 'image_path') and el.metadata.image_path:
                                img_filename = os.path.basename(el.metadata.image_path)
                                content += f'<br><br><img src="{IMAGE_OUTPUT_DIR}/{img_filename}" class="lesson-image"><br><br>'
                            continue

                        text = el.text.strip()
                        if not text: continue
                        
                        if "Title" in str(type(el)):
                            content += f"<br><br><strong>{text}</strong><br><br>"
                        elif "ListItem" in str(type(el)):
                            content += f"<br>• {text}"
                        else:
                            content += f"{text} "
                    
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump({"chapterName": file, "content": content.replace("  ", " ")}, f, ensure_ascii=False, indent=4)
                            
                except Exception as e:
                    print(f"  [!] Error parsing {file}: {e}")

if __name__ == "__main__":
    run_parser()
    print("\n✅ Batch process complete!")



# if you dont already have the python packages then install them: 
Open your terminal inside this project folder and run the commands one by one to ensure each installs correctly:


pip install unstructured[pdf]


pip install pdfminer.six


pip install pytesseract


pip install opencv-python


# Library Breakdown:
unstructured[pdf]: The core engine that parses your PDF structure and handles high-resolution image extraction.



pdfminer.six: Required by unstructured to read the underlying text layers of your PDFs.



pytesseract: The bridge between your Python code and the Tesseract OCR engine (to read scanned text).



opencv-python: Used for image processing, specifically to handle the diagrams and figures being cropped from your files.

