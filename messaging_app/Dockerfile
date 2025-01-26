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
WORKDIR /messaging_app


# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .