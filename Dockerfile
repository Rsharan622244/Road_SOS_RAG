FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python build_knowledge_base.py

EXPOSE 7860

CMD ["python", "app.py"]
