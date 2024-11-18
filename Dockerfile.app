FROM python:3.11-slim

WORKDIR /app
COPY app.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "app:app", "--bind", "0.0.0.0:5000"]
