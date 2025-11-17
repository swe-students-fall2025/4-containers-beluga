# in Docker, it is common to base a new image on a previously-created image
FROM python:3.10-slim

# Set the working directory in the image
WORKDIR /app

# Install pipenv
RUN pip3 install pipenv

# Copy Pipfile and Pipfile.lock for dependency installation
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv - doing this first will speed up subsequent builds, as Docker will cache this step
# --deploy ensures the lock file is up to date
RUN pipenv install

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .

# expose the port that the Flask app is running on... by default 5000
ARG PORT=5000
EXPOSE ${PORT}

# Run app.py when the container launches
CMD ["pipenv", "run", "python3", "-m", "flask", "run", "--host=0.0.0.0"]
