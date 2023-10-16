from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxHandler:
    def __init__(self, url, token, batch_size=1000):
        self.client = InfluxDBClient(url=url, token=token)
        self.org = None
        self.bucket = None
        self.batch_size = batch_size
        self.points = []

    def set_org(self, org_name):
        self.org = org_name

    def set_bucket(self, bucket_name):
        self.bucket = bucket_name

    def add_point(self, measurement, tags, fields):
        if self.bucket is None:
            raise Exception("Bucket is not set. Use set_bucket() method first.")

        point = Point(measurement)
        for tag_key, tag_value in tags.items():
            point.tag(tag_key, tag_value)
        for field_key, field_value in fields.items():
            point.field(field_key, field_value)
        self.points.append(point)

        if len(self.points) >= self.batch_size:
            self.write_points()

    def write_points(self):
        if self.bucket is None or self.org is None:
            raise Exception("Bucket or Organization is not set. Use set_bucket() and set_org() methods first.")

        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.bucket, org=self.org, record=self.points)
        self.points = []

    def query_data(self, flux_query):
        if self.org is None:
            raise Exception("Organization is not set. Use set_org() method first.")

        query_api = self.client.query_api()
        tables = query_api.query(org=self.org, query=flux_query)
        results = []
        for table in tables:
            for row in table.records:
                results.append(row.values)
        return results

    def close(self):
        if self.points:
            self.write_points()
        self.client.__del__()