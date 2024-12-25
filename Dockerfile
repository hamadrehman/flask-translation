FROM python:3.11-slim

# Disable PIP caching
ENV PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Register libraries to python sys.path
# RUN echo "export PYTHONPATH=${PYTHONPATH}" >> ~/.bashrc

# Update sources
RUN apt-get update --allow-releaseinfo-change && apt-get install -y \
gcc \
&& rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY ./app .

COPY ./app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


# Run gunicorn
CMD ["sh", "-c", "python3 serve.py"]

