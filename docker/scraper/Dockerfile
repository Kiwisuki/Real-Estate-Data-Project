# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV SCRAPER_ENV_VARIABLE=value

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./scraper /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run scraper.py when the container launches
CMD ["python", "scraper.py"]
