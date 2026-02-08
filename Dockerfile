FROM python:3.13-slim

# Устанавливаем uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /ItkAcademy
COPY pyproject.toml uv.lock ./

RUN uv pip install --system .

COPY src ./src

