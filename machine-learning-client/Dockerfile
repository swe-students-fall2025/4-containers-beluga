# In Docker, it is common to base a new image on a previously-created image
# Use an official Python runtime image as a parent image to base this image on
FROM python:3.10-slim

# Install dependencies required for cv2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory within the image to /app
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock for dependency installation
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv - doing this first will speed up subsequent
# builds, as Docker will cache this step
RUN pipenv sync --system

# The ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .

# By default Docker containers are closed off to the external world
# Make port 80 available to the world outside this container
ARG PORT=80
EXPOSE ${PORT}

# Define an environment variable... this will be available to programs running inside the container
ENV FOO bar

# Run client.py when the container launches
CMD ["python", "client.py"]
