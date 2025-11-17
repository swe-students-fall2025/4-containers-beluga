# in Docker, it is common to base a new image on a previously-created image
# Use an official Python runtime image as a parent image to base this image on
FROM python:3.10-slim
# Set the working directory within the image to /app
WORKDIR /app
# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .
# Install any needed packages specified in requirements.txt
# in Python, a requirements.txt file is a way of indicating dependencies in a way that the package manager, pip, can understand
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# by default Docker containers are closed off to the external world
# Make port 80 available to the world outside this container
ARG PORT=80
EXPOSE ${PORT}
# Define an environment variable... this will be available to programs running inside the container
ENV FOO bar
# Run app.py when the container launches
CMD ["python", "app.py"]