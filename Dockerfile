FROM python:3.9-alpine

WORKDIR /app

# Enhanced system dependencies including what's needed for pyarrow
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    make \
    g++ \
    # Add these for pyarrow
    cmake \
    ninja \
    flex \
    bison \
    boost-dev \
    zlib-dev

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Run the web service on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]