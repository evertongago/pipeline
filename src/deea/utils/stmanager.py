from google.cloud import storage

class StorageManager:

    def __init__(self):
        self.client = storage.Client()

    def upload(self, btname, sfname, dfname):
        bucket = self.client.bucket(btname)
        blob = bucket.blob(dfname)
        blob.upload_from_filename(sfname)

        print('File uploaded: gs://{}/{}'.format(btname, dfname))

    def read_appfollow_keys(self, nbucket, filename):
        bucket = self.client.get_bucket(nbucket)
        file = bucket.get_blob(filename)

        value = file.download_as_string().decode('utf-8')
        value = value.replace('\n', '')
        value = value.split('\t')

        return {'cid': value[0], 'sign': value[1]}
