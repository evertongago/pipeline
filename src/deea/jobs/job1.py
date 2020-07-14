from pyspark.sql import SparkSession

if __name__ == '__main__':

    # Create Spark Session
    spark = SparkSession.builder.master('yarn').appName('Job 1').getOrCreate()

    print('Job 1 - Done.')
