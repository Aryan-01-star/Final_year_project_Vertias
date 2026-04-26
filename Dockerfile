# 1. Use a slim version of Python to keep the image small and secure
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (optimizes build speed)
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir keeps the image size small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your underwriting code
COPY . .

# 6. Set environment variables (GCP Cloud Run expects port 8080)
ENV PORT 8080
ENV PYTHONUNBUFFERED True

# 7. Start your application 
# Replace 'main:app' with your actual file and app name (e.g., 'api:app')
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
