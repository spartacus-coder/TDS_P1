FROM python:3.13-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN pip install fastapi uvicorn requests python-dotenv

WORKDIR /app

# Create the /data directory and set permissions
RUN mkdir -p /data && chmod 755 /data
RUN mkdir -p /data/logs
RUN mkdir -p /data/docs
COPY . /app

CMD ["uv", "run", "app.py"]
