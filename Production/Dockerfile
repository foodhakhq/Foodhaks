# Use an official lightweight Python image.
FROM python:3.12-slim
# Set environment variables to prevent .pyc files and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the working directory.
WORKDIR /app
# Install build dependencies and pip packages.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code.
COPY . .
# Expose the port your Flask app runs on.
EXPOSE 8000
# Use Gunicorn to serve the Flask application.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]