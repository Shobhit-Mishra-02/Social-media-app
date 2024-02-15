FROM python:3.9

# set up the env variables
ENV PYTHONUNBUFFERED 1

# set up the working directory
WORKDIR /code

# Copy django project into the container
COPY . /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

