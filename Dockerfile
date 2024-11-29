# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies and additional tools
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Default command to run the application
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
