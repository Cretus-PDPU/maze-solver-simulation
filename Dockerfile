# Use the official Python image as the base image
FROM python:3.10

# Set environment variables to ensure Python prints everything to stdout without buffering
ENV PYTHONUNBUFFERED 1

# Create and set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory (including requirements.txt) to the container's working directory
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port your Flask app will run on (adjust as needed)
EXPOSE 5000

# Run your Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
