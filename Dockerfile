# Stage 1: Install Node.js dependencies and build Tailwind CSS
FROM node:lts AS node-build

# Set working directory for Node.js
WORKDIR /build

# Copy package.json and package-lock.json first to cache dependencies
COPY src/package.json src/package-lock.json ./
RUN npm install --legacy-peer-deps daisyui@latest htmx.org@2.0.3

# Install TailwindCSS and build CSS
COPY src/static ./static
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

# Copy HTMX
RUN mkdir -p ./static/js
RUN cp node_modules/htmx.org/dist/htmx.min.js ./static/js/htmx.min.js

# Stage 2: Build Python dependencies and copy final assets
FROM python:3.11

# Set the working directory
WORKDIR /code

# Install system dependencies for Node and Python
RUN apt-get update && apt-get install -y curl gnupg

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Node assets from the previous build stage
COPY --from=node-build /build/static ./static

# Copy Django project files
COPY src ./

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
