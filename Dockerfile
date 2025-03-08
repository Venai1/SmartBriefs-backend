# Use the Python 3 alpine official image
FROM python:3.9-alpine

# Create and change to the app directory
WORKDIR /app

# Install system dependencies needed for Python packages
# These are especially needed for pandas, numpy, and other data science libraries
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    make \
    g++

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Run the web service on container startup using hypercorn as Railway suggests
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]