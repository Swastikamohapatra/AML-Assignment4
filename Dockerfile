# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# The /app directory should act as the main application directory
WORKDIR /app

# Copy all folder documents into the docker image; we will need this for testing
COPY . .

RUN pip install -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
