# Pull base image
FROM python:3.10.4-slim-bullseye

# Set environment variables
#disables an automatic check for pip updates each time the image is built
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

#disables creation of .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

#disables buffering of stdout and stderr
#to ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1


# Set work directory
WORKDIR /app

# Install system dependencies for mysqlclient and pip
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies
COPY ./requirements.txt Requirements.txt
RUN pip install --no-cache-dir -r Requirements.txt

# Copy project
COPY . .

# Expose the port your Django app runs on
EXPOSE 8000

# Run the Django application

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]