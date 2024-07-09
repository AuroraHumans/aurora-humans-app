FROM python:3.11-slim


COPY requirements.txt /app/requirements.txt
WORKDIR /app


RUN pip install --no-cache-dir -r /app/requirements.txt

# Add Pulumi to PATH
ENV PATH="/usr/local/pulumi:${PATH}"

COPY . /app/
WORKDIR /app

EXPOSE 8501
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]