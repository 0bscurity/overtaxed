FROM python:3.11

# Set the working directory
WORKDIR /code

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl gnupg
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/package.json src/package-lock.json ./
RUN npm install
RUN npm i -D daisyui@latest htmx.org@2.0.3

# Copy project files
COPY src .

RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

RUN cp node_modules/htmx.org/dist/htmx.min.js ./static/js/htmx.min.js

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
