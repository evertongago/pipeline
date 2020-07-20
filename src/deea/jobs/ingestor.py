import sys

from datetime import datetime
from pyspark.sql import SparkSession
from src.deea.utils import utils
from src.deea.utils.api import Ingestor
from src.deea.utils.stmanager import StorageManager

if __name__ == '__main__':

    # workflow arguments
    app_name, app_id, mode = sys.argv[1:]
    bucket = 'krtn'

    # get app follow keys and instanciate api
    sm = StorageManager()
    credentials = sm.read_appfollow_keys(bucket, 'credentials/appfollow.txt')
    app = Ingestor(cid=credentials['cid'], sign=credentials['sign'])

    # TODO code ingestion routine
    page = 1
    date = str(datetime.today())
    date = '{}{}{}'.format(date[:4], date[5:7], date[8:10])

    # ingestion page reviews
    reviews = app.fetch(ext_id=app_id, page=page)
    filename = '{}.json'.format(page)
    utils.save_file(reviews, filename)
    sm.upload(bucket, filename, 'datalake/reviews/tra/{}/{}/{}'.format(app_name, date, filename))
