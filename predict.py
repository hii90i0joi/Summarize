import os
import tempfile
from cog import BasePredictor, Input, Path
from model import run_pipeline
import shutil
import json

class Predictor(BasePredictor):
    def predict(
        self,
        pdf_file: Path = Input(description="Upload a single PDF file"),
    ) -> dict:
        # 1. Create a temporary folder to work inside
        with tempfile.TemporaryDirectory() as tmpdir:
            # 2. Save the PDF to temp path
            pdf_path = os.path.join(tmpdir, "input.pdf")
            shutil.copy(str(pdf_file), pdf_path)

            # 3. Run pipeline
            run_pipeline(pdf_path)

            # 4. Construct output path based on file name
            base_name = os.path.splitext(os.path.basename(pdf_path))[0].rstrip("-_ ")
            json_output_path = os.path.join("static", "structured_output", f"{base_name}.json")

            # 5. Load and return JSON output
            if not os.path.exists(json_output_path):
                raise FileNotFoundError(f"Output JSON not found: {json_output_path}")

            with open(json_output_path, "r", encoding="utf-8") as f:
                return json.load(f)
