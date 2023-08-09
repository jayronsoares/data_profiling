
# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Update the package manager and install the required dependencies of the image
RUN apt-get update && apt-get install -y python3-dev build-essential

# Install the application dependencies using pip3
RUN pip3 install -r requirements.txt

# Define the entry point for the container
CMD ["flask", "run", "--host=0.0.0.0"]
