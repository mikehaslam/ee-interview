FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd -m -u 501 mike && chown -R mike:mike /app

USER mike

EXPOSE 8080

ENV PORT=8080

CMD ["python", "app.py"]
