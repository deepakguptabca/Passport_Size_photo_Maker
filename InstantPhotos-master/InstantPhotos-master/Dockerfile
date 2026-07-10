# Base Image
FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

#working directory
WORKDIR /app

#INSTALL DEPENDICES
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy project
COPY . .

#Flask runs on this port

#start flask
CMD ["python","app.py"]