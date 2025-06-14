#moamolpdf.py
import os
from pdf2image import convert_from_path

def moamolpdf(pdf_path, output_folder=None):
    """
    تحويل ملف PDF إلى صور بحيث تكون كل صفحة صورة منفصلة.
    
    :param pdf_path: مسار ملف PDF
    :param output_folder: المجلد الذي سيتم حفظ الصور فيه
    """
    if output_folder is None:
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join("images", filename)
    os.makedirs(output_folder, exist_ok=True)

    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        page_path = os.path.join(output_folder, f"page_{i + 1}.png")
        page.save(page_path, "PNG")

    print("✅ PDF successfully converted to images.")
