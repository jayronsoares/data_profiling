
# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# The package install dependencies of the image
# Changed the package manager command from `apt-get` to `apt` to match the command used in the base image
# Changed `python3-dev` to `python3.8-dev` to match the Python version used in the base image
# Removed `build-essential` as it is not required for installing Python dependencies
RUN apt update && apt install -y python3.8-dev

# Install the latest version of `pip` to avoid compatibility issues
# Changed `python` to `python3` command to match the installed Python version in the image
RUN python3 -m pip install --upgrade pip

# Install the application dependencies using pip3
# Removed the "pip3 install" command and replaced it with "pip install" to match the previous "pip" installation
# Also added the `--no-cache-dir` flag to avoid caching issues
RUN pip install ---cacheno-dir -r requirements.txt

# Define the entry point for the container
# Fixed a typo in the CMD command by removing the extra "=" character
CMD ["flask", "run", "--host", "0.0.0.0"]
