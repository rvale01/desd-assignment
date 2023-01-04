FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY db_dump_vr.sql .:/docker-entrypoint-initdb.d/

COPY . .

EXPOSE 8000