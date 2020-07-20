from google.cloud import bigquery

class BigQueryManager:

    def __init__(self, dataset='reviews', in_mode='daily'):
        # Create client connection.
        self.client = bigquery.Client()

        # Get dataset reference.
        self.dataset_ref = self.client.dataset(dataset)

        # Set configuration job.
        self.job_config = bigquery.LoadJobConfig()

        self.job_config.source_format = bigquery.SourceFormat.PARQUET

        if in_mode == 'daily':
            self.job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        else:
            self.job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    def write(self, table_name, uri):
        # Execute job.
        load_job = self.client.load_table_from_uri(
            uri, self.dataset_ref.table(table_name), job_config=self.job_config
        )

        # Catch results.
        job_id = load_job.job_id
        load_job.result()

        destination_table = self.client.get_table(self.dataset_ref.table(table_name))
        num_rows = destination_table.num_rows

        # Return results.
        return {'job_id': job_id, 'num_rows': num_rows}
