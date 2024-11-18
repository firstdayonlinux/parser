FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG USER=llm_sales_user

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    python3-dev \
    wget \
    curl \
    libssl-dev \
    gcc \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /app/
RUN pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && rm -rf /root/.cache/pip

COPY . /app

RUN groupadd --gid 2000 "$USER" \
  && useradd --uid 2000 --gid "$USER" "$USER" \
  && chown -R llm_sales_user /app

USER llm_sales_user

ENTRYPOINT ["python3", "main.py"]
