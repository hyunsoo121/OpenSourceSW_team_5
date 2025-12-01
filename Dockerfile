# 가벼운 Python 3.9 이미지
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# [변경점] 무거운 build-essential 제거!
# libpq-dev만 최소한으로 설치 (혹시 모를 라이브러리 의존성 해결)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
