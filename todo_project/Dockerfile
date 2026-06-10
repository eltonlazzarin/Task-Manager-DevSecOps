FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=False
ENV SECRET_KEY=devsecops-secret-key

CMD ["python", "run.py"]