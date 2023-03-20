# Use the official Python image as the base image
FROM python:3.9-slim-buster


# Set the working directory to /app
WORKDIR /


# Copy the current directory contents into the container at /app
COPY . /


# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt




# Start the Flask app
CMD ["python", "app.py"]





