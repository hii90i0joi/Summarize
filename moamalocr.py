#moamalocr.py
import os
import io
from google.cloud import vision

def MoamalOCR(service_account_json, images_folder, output_folder="outputtext", batch_size=5):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json
    base_name = os.path.basename(images_folder.rstrip("/\\"))
    output_folder = output_folder  


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    client = vision.ImageAnnotatorClient()
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        print("❌ لم يتم العثور على أي صور.")
        return

    batches = [image_files[i:i + batch_size] for i in range(0, len(image_files), batch_size)]

    for batch_index, batch in enumerate(batches):
        print(f"📦 دفعة {batch_index + 1}/{len(batches)}")

        requests = []
        for image_file in batch:
            image_path = os.path.join(images_folder, image_file)
            with io.open(image_path, "rb") as img_f:
                content = img_f.read()

            image = vision.Image(content=content)
            feature = vision.Feature(type=vision.Feature.Type.TEXT_DETECTION)
            requests.append(vision.AnnotateImageRequest(image=image, features=[feature]))

        try:
            response = client.batch_annotate_images(requests=requests)
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Vision API: {e}")
            continue

        for image_file, annotation in zip(batch, response.responses):
            page_number = os.path.splitext(os.path.basename (image_file))[0]

            output_path = os.path.join(output_folder,f"{page_number}.text")
                                       
            extracted_text = annotation.text_annotations[0].description if annotation.text_annotations else "No text detected"
            
            print(f"📄 محتوى نص {page_number}:\n{extracted_text[:300]}")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
                f.write(f"--- Page {page_number} ---\n")


            
            print(f"✅ {image_file} ➝ {output_path}")
            print(f"📄 محتوى {output_path}:\n{extracted_text[:300]}")


    print("🎉  OCR DONE .")
