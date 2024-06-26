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

CMD ["streamlit", "run", "app.py"]