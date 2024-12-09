import sys
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col

# Function to clean and prepare data
def clean_data(df):
    """Clean and prepare DataFrame by casting all columns to double."""
    return df.select(*(col(c).cast("double").alias(c.strip("\"")) for c in df.columns))

if __name__ == "__main__":
    try:
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName('Wine_Quality_Prediction_Testing') \
            .config("spark.sql.shuffle.partitions", "50") \
            .getOrCreate()

        # Set Spark log level to ERROR for cleaner output
        spark.sparkContext.setLogLevel('ERROR')

        # Define paths (these should match your Docker container structure)
        test_dataset_path = '/app/datasets/TestDataset.csv'
        model_path = '/app/models'

        # Load the test dataset
        print(f"Loading test dataset from {test_dataset_path}...")
        test_df = spark.read.format("csv").option('header', 'true').option("sep", ";").load(test_dataset_path)
        cleaned_test_df = clean_data(test_df)

        # Load the pre-trained model
        print(f"Loading model from {model_path}...")
        model = PipelineModel.load(model_path)

        # Make predictions using the model
        print("Making predictions on the test dataset...")
        predictions = model.transform(cleaned_test_df)

        # Evaluate the model
        evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
        accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})
        f1_score = evaluator.evaluate(predictions)

        # Output the results
        print(f"Model performance: Accuracy = {accuracy:.4f}")
        print(f"Weighted F1 Score of the best model: {f1_score:.4f}")

        # Stop Spark session
        spark.stop()

    except Exception as e:
        print(f"Error occurred: {e}")
