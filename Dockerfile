# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the rest of the app
COPY . .

# Expose port for Gunicorn
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"] 