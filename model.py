# model.py
import os
from moamolpdf import moamolpdf
from moamalocr import MoamalOCR
from moamalnpl import process_txt_files

def run_pipeline(pdf_path):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0].rstrip("-_ ")

   
    image_folder = os.path.join("images", base_name)
    text_output_folder = os.path.join("outputtext", base_name)
    json_output_file = os.path.join("static", "structured_output", f"{base_name}.json")

    moamolpdf(pdf_path, output_folder=image_folder)
    MoamalOCR(
        service_account_json="credentials.json",
        images_folder=image_folder,
        output_folder= text_output_folder,
        batch_size=10
    )
    process_txt_files(
        input_folder=text_output_folder,
        output_json_path=json_output_file,
    )
