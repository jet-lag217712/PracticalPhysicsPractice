FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set working directory
WORKDIR /app

# Install Xvfb for headed browser support
RUN apt-get update && apt-get install -y \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium
RUN playwright install chromium

# Copy app files
COPY main.py .
COPY web_helper.js ./web_helper.js

# Environment setup
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Start Xvfb and run the script
CMD ["bash", "-c", "Xvfb :99 -screen 0 1280x720x24 & python main.py"]
