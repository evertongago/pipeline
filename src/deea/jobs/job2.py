from pyspark.sql import SparkSession

if __name__ == '__main__':

    # Create Spark Session
    spark = SparkSession.builder.master('yarn').appName('Job 2').getOrCreate()

    print('Job 2 - Done.')
