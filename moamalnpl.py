import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

BATCH_SIZE = 5

def process_txt_files(input_folder, output_json_path=None):
    batches = []
    current_batch = ""
    count = 0

    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".text"):
            with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    current_batch += f"\n\n--- Page {filename} ---\n{content}"
                    count += 1
                    if count == BATCH_SIZE:
                        batches.append(current_batch)
                        current_batch = ""
                        count = 0

    if current_batch.strip():
        batches.append(current_batch)

    results = []

    for idx, batch_text in enumerate(batches):
        print(f"\n📦 معالجة الدفعة {idx + 1} من {len(batches)}")
        print("📤 النصوص قبل الإرسال:\n", batch_text[:500])

        prompt = f"""
You are a helpful assistant.

Please summarize the following academic text clearly and concisely.

Text:
{batch_text}
"""

        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4000,
            )

            if not response.choices or not response.choices[0].message:
                print("❌ لا يوجد رد من LLM.")
                continue

            summary = response.choices[0].message.content.strip()

            results.append({
                "batch": idx + 1,
                "summary": summary
            })

        except Exception as e:
            print(f"❌ خطأ في الدفعة {idx + 1}: {e}")
            continue

    if not results:
        print("⚠️ لم يتم تلخيص أي شيء.")
        return []

    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            json.dump(results, out_f, ensure_ascii=False, indent=2)
        print(f"✅ JSON IS DONE: {output_json_path}")
        print("📂 تم التلخيص:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    return results