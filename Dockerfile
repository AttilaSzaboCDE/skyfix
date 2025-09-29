FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]