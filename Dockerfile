# Use a Python base image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app
WORKDIR /app

# Set environment variable to include Geckodriver path
ENV PATH="/app/web_driver:${PATH}"

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 5000 and run the Flask app
EXPOSE 5000
CMD ["python", "app.py"]
