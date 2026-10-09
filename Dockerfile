# Base OS
FROM python:3.14-slim

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set Default Working Directory
WORKDIR /app

# Updating Packages
RUN pip install --upgrade pip

# Copy Requirements Files
COPY ./requirements.txt ./requirements.txt

# Installing Packages
RUN pip install -r requirements.txt

# Copy Required Files
COPY . .