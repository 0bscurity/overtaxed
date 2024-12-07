FROM python:3.11

# Set the working directory
WORKDIR /code

# Install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src .

# Set environment variables
ENV PYTHONUNBUFFERE=1

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
