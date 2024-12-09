# Use the official OpenJDK base image
FROM openjdk:8-jdk

# Install Python 3 and required dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pyspark==3.4.0 boto3==1.26.10 numpy==1.23.0

# Set the working directory in the container
WORKDIR /app

# Copy the datasets, models, and script into the container
COPY models /app/models
COPY datasets /app/datasets
COPY testmodel.py /app/testmodel.py

# Set the entry point
ENTRYPOINT ["python3", "/app/testmodel.py"]
