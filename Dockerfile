# Use the official Python 3.10 image as a base
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Exclude the config_local.env file
RUN rm -f config_local.env

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start the application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
