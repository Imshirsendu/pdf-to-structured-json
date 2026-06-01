import os
import json
import logging
from unstructured.partition.pdf import partition_pdf

# --- CONFIGURATION ---
# Format: "Source_Directory_Name": "Output_Directory_Name"
# You can add or remove as many pairs as you want here.
PROCESSING_MANIFEST = {
    "source_directory_1": "output_directory_1",
    "source_directory_2": "output_directory_2",
    "source_directory_3": "output_directory_3"
}

IMAGE_OUTPUT_DIR = "assets/images"
# ---------------------

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