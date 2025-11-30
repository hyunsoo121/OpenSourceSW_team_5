# Python 3.9.2 버전 사용 (사용자 환경과 동일)
FROM python:3.9.2-slim

# 파이썬 출력이 버퍼링 없이 즉시 출력되도록 설정 (로그 확인 용이)
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치 (PostgreSQL 연동 등에 필요한 gcc 등)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 패키지 목록 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 프로젝트 코드 복사
COPY . /app/

# 포트 노출 (문서화 목적)
EXPOSE 8000

# 컨테이너 실행 명령어 (Gunicorn 실행)
# config.wsgi:application 은 config 폴더 안의 wsgi.py를 의미함
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
