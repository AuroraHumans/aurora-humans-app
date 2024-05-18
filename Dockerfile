FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Add Pulumi to PATH
ENV PATH=$PATH:/root/.pulumi/bin

COPY . /app/
WORKDIR /app

EXPOSE 8501
ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "app.py"]