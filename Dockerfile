# 1. استخدم Python الرسمي
FROM python:3.11-slim

# 2. تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# 3. نسخ الملفات
COPY . /app

# 4. تثبيت poppler و gcc للـ pdf2image و pillow (اختياري حسب الكود)
RUN apt-get update && apt-get install -y poppler-utils gcc

# 5. تثبيت المتطلبات
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. تعيين المتغير الخاص بمفتاح جوجل (سنجلبه لاحقًا وقت التشغيل)
ENV GOOGLE_APPLICATION_CREDENTIALS="credentials.json"

# 7. فتح المنفذ
EXPOSE 5000

# 8. تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

