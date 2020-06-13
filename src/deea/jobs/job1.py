from pyspark.sql import SparkSession

if __name__ == '__main__':

    # Create Spark Session
    spark = SparkSession.builder.master('yarn').appName('Job 1').getOrCreate()

    df = spark.read.option('header','true').csv('gs://deeapipe/lake/transient/tabela1.csv')

    df = df.groupBy(['curso']).count()

    df.coalesce(1).write.mode('overwrite').csv('gs://deeapipe/lake/refined/tabela1')

    print('Job 1 - Done.')
