import sys

from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql import functions as F, types as T

from src.deea.utils import utils
from src.deea.utils.bqmanager import BigQueryManager

if __name__ == '__main__':

    # workflow arguments
    app_name, mode = sys.argv[1:]
    bucket = 'krtn'

    # create spark session
    spark = SparkSession.builder.master('yarn').appName('Processor').getOrCreate()

    # mount file path
    date = str(datetime.today())
    date = '{}{}{}'.format(date[:4], date[5:7], date[8:10])
    path_tra = 'gs://{}/datalake/reviews/tra/{}/{}/*.json'.format(bucket, app_name, date)

    # read json from datalake
    data = spark.read.json(path_tra)

    # parser json to simple columns
    exploded = data.select([F.explode('reviews.list').alias('review')])
    exploded = exploded.withColumn('has_answer', exploded.review.has_answer)
    exploded = exploded.withColumn('app_version', exploded.review.app_version)
    exploded = exploded.withColumn('country', exploded.review.country)
    exploded = exploded.withColumn('created', exploded.review.date)
    exploded = exploded.withColumn('content', exploded.review.content)
    exploded = exploded.withColumn('rating', exploded.review.rating)

    # remove old columns
    exploded = exploded.drop('review')
    exploded = exploded.drop('store')

    # filter consistent reviews
    exploded = exploded.filter(F.col('content').isNotNull())

    # strip text
    strip_udf = F.udf(utils.strip_text, T.StringType())
    exploded = exploded.withColumn('content_stp', strip_udf(F.col('content')))

    # put review type from rating
    exploded = exploded.withColumn('type', F.when(F.col('rating') > 3, 'Promotor').otherwise('Detrator'))

    path_raw = 'gs://{}/datalake/reviews/raw/{}/{}'.format(bucket, app_name, date)
    exploded.write.mode('overwrite').parquet(path_raw)

    # Persist to BigQuery.
    bqm = BigQueryManager(dataset='reviews', in_mode=mode)
    stmts = bqm.write(app_name, '{}/*.parquet'.format(path_raw))

    print('Reviews table: Loaded {} rows.'.format(stmts['num_rows']))
