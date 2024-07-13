FROM python:3.11-slim


WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

EXPOSE 8080
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]