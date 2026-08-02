FROM python:3.12-slim

# git is required so the agent can clone remote repositories.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source.
COPY . .

# Review the bundled sample repo by default; override the CMD to pass a URL.
CMD ["python", "main.py"]
