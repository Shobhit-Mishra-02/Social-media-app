FROM python:3.9

# set up the env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set up the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy django project into the container
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run the project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]