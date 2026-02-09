import os
import shutil
import zipfile
import img2pdf
from PIL import Image
from .metadata import generate_comic_info_xml

def create_cbz_archive(source_folder: str, output_path: str, metadata: dict = None) -> bool:
    """
    Compresses a directory into a CBZ (ZIP) archive.
    Optionally includes a ComicInfo.xml metadata file.
    """
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as cbz:
            # 1. Add Images
            for root, dirs, files in os.walk(source_folder):
                for file in sorted(files): # Ensure correct page order
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=source_folder)
                    cbz.write(file_path, arcname)
            
            # 2. Add Metadata XML
            if metadata:
                xml_str = generate_comic_info_xml(metadata)
                cbz.writestr("ComicInfo.xml", xml_str)
                
        return True
    except Exception as e:
        print(f"CBZ Creation Error: {e}")
        return False

def create_pdf_document(source_folder: str, output_path: str) -> bool:
    """
    Compiles images from a directory into a single PDF document.
    """
    try:
        images = []
        # Walk through and sort files
        for root, _, files in os.walk(source_folder):
            for file in sorted(files):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    img_path = os.path.join(root, file)
                    
                    # Convert WebP to JPG as some PDF libraries struggle with WebP
                    if file.lower().endswith(".webp"):
                        try:
                            im = Image.open(img_path).convert("RGB")
                            new_path = os.path.splitext(img_path)[0] + ".jpg"
                            im.save(new_path, "JPEG")
                            images.append(new_path)
                            os.remove(img_path) # Remove original webp to save space
                        except Exception:
                            continue 
                    else:
                        images.append(img_path)
        
        if not images: return False
        
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(images))
            
        return True
    except Exception as e:
        print(f"PDF Creation Error: {e}")
        return False