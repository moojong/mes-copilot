
FROM python:3.11-slim

# 시스템 패키지 설치 (DB 드라이버 등)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt만 복사 (앱 소스는 마운트)
COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# 앱 소스는 마운트됨, 기본 실행은 Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
