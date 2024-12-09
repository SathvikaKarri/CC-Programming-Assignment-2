
# Wine Quality Prediction Using PySpark(sk3628)

## Objective
This project aims to develop a Python application using PySpark for predicting wine quality. The application leverages AWS Elastic MapReduce (EMR) to train the machine learning model in parallel across multiple EC2 instances. A Docker container is also created to simplify the deployment of the trained model.

---

## Features
- Predicts wine quality using PySpark.
- Utilizes AWS EMR for distributed training.
- Stores datasets and models in S3.
- Deploys the trained model using Docker for testing.

---

## Repositories
- **GitHub Repository**: [Wine Quality Prediction GitHub Repository](https://github.com/SathvikaKarri/CC-Programming-Assignment-2)
- **Docker Hub Repository**: [Wine Prediction Docker Image](https://hub.docker.com/repository/docker/sathvikarri/wineprediction/general)

---

## Execution Steps

### 1. Create Key-Pair for the EMR Cluster
- Navigate to EC2 > Key Pairs.
- Generate a key pair named `hemanth.pem` and download it in `.pem` format.

### 2. Create an S3 Bucket
- Create an S3 bucket named `winepredictionquality`.

### 3. Set Up the EMR Cluster
- Go to the EMR Console and create a cluster named `winepredictionquality`.
- Use EMR release version `emr-7.5.0`, which includes Hadoop 3.4.0 and Spark 3.5.2.

### 4. Configure the Spark Cluster
- Create the cluster.
- Set up cluster scaling, networking, IAM roles, termination policies, and use the `sathvi.pem` EC2 key pair.

### 5. Train the Machine Learning Model
- SSH into the EC2 instance:
  ```bash
  ssh -i "sathvi.pem" ec2-user@<ec2-public-dns>
  ```
- Submit the training job:
  ```bash
  spark-submit winequality.py s3://winepredictionquality/datasets/TrainingDataset.csv s3://winepredictionquality/datasets/ValidationDataset.csv
  ```
  - The training script splits `TrainingDataset.csv` into 90% training and 10% testing.
  - Saves the test data as `TestDataset.csv` in the S3 dataset folder.
- Save the trained model to:
  ```text
  s3://winepredictionquality/models
  ```

### 6. Test the Model
- Run the test using:
  ```bash
  spark-submit testwinequality.py s3://winepredictionquality/datasets/TestDataset.csv s3://winepredictionquality/models
  ```

---

## Using Docker for Deployment

### Set Up Docker
1. Create a Docker account and install Docker on your local machine.
2. Log in to Docker and build the image:
   ```bash
   docker build -t wine-quality-test .
   ```

### Push the Image
1. Tag the image:
   ```bash
   docker tag wineprediction sathvikarri/wineprediction
   ```
2. Push the image to Docker Hub:
   ```bash
   docker push sathvikarri/wineprediction
   ```

### Pull and Run the Image
1. Pull the Docker image:
   ```bash
   docker pull sathvikarri/wineprediction
   ```
2. Run the Docker container with the test dataset and saved model:
   ```bash
   docker run --rm wineprediction /app/datasets/TestDataset.csv /app/models
   ```


## Model Accuracy
- **Accuracy**: 0.73

## Requirements
- **Python**: PySpark library
- **AWS**: EMR, S3
- **Docker**: Installed and configured
