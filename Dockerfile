FROM python:3.7-slim AS release

# Create app directory
WORKDIR /app

COPY app .

# Install app dependencies
RUN pip install -r requirements.txt
