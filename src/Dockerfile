FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

# RUN uv sync

ENV PATH="/app/.venv/bin:{$PATH}"

# Expose the specified port for FastAPI
EXPOSE $PORT

CMD ["uvicorn", "app.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]