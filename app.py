from flask import Flask, request, jsonify
import os
import tempfile
from moamolpdf import moamolpdf
from moamalocr import MoamalOCR
from moamalnpl import process_txt_files
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]
    if pdf_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "input.pdf")
        pdf_file.save(pdf_path)

        images_dir = os.path.join(temp_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        moamolpdf(pdf_path, images_dir)

        texts_dir = os.path.join(temp_dir, "texts")
        os.makedirs(texts_dir, exist_ok=True)
        MoamalOCR(
     service_account_json="/etc/secrets/credentials.json",  
    images_folder=images_dir,
    output_folder=texts_dir
)


        results = process_txt_files(texts_dir)  # لا نرسل output_json_path

        return jsonify(results)  # 🎯 مباشرة JSON بدون تخزين

if __name__ == "__main__":
    app.run(debug=True)
