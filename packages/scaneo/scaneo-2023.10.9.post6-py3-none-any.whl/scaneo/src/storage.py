import os
from minio import Minio
from glob import glob
import fnmatch
import rasterio as rio
import pandas as pd
import json
import io
import requests


class Storage:
    def __init__(self):
        # if valid environment variables are set, use cloud storage
        url = os.getenv("URL")
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")
        bucket = os.getenv("BUCKET")
        if url and access_key and secret_key and bucket:
            self.storage = CloudStorage(
                url,
                access_key,
                secret_key,
                bucket,
                os.getenv("REGION", "us-east-1"),
                os.getenv("PREFIX", None),
            )
        # otherwise, use local storage
        else:
            path = os.getenv("DATA")
            if not path:
                raise Exception("No storage specified.")
            self.storage = LocalStorage(os.getenv("DATA"))

    def list(self, pattern="**/*"):
        return self.storage.list(pattern)

    def get_url(self, name):
        return self.storage.get_url(name)

    def exists(self, name):
        return self.storage.exists(name)

    def read(self, name):
        ext = name.split(".")[-1]
        if ext in ["tif", "tiff"]:
            return rio.open(self.get_url(name))
        elif ext in ["json", "geojson"]:
            # return pd.read_json(self.get_url(name)).to_json() # problem with SSL certificate
            url = self.get_url(name)
            if url.startswith("http://") or url.startswith("https://"):
                response = requests.get(url)
                return json.loads(response.json())
            with open(url, "r") as file:
                return json.load(file)
        raise TypeError("Not a valid type")

    def save(self, name, data):
        return self.storage.save(name, data)


class LocalStorage:
    def __init__(self, path):
        self.path = path

    def list(self, pattern):
        paths = glob(os.path.join(self.path, pattern), recursive=True)
        return [p.replace(self.path + "/", "") for p in paths]

    def get_url(self, name):
        return os.path.join(self.path, name)

    def exists(self, name):
        return os.path.exists(os.path.join(self.path, name))

    def save(self, name, data):
        with open(os.path.join(self.path, name), "w") as f:
            json.dump(json.loads(data), f)
        return self.get_url(name)


class CloudStorage:
    def __init__(self, url, access_key, secret_key, bucket, region, prefix=None):
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.prefix = prefix
        self.region = region
        self.client = Minio(
            endpoint=url,
            access_key=access_key,
            secret_key=secret_key,
            secure=True,
            region=region,
        )
        if not self.client.bucket_exists(self.bucket):
            raise Exception("Bucket does not exist.")

    def list(self, pattern):
        return fnmatch.filter(
            [
                obj.object_name
                for obj in self.client.list_objects(self.bucket, recursive=True)
                # for obj in self.client.list_objects(self.bucket, prefix=self.prefix)
            ],
            pattern,
        )

    def get_name(self, name):
        return name if not self.prefix else os.path.join(self.prefix, name)

    def get_url(self, name):
        return self.client.presigned_get_object(self.bucket, self.get_name(name))

    def exists(self, name):
        try:
            return self.client.stat_object(self.bucket, self.get_name(name))
        except:
            return False

    def save(self, name, data):
        data = json.dumps(data)
        data_bytes = data.encode("utf-8")
        data_file = io.BytesIO(data_bytes)
        self.client.put_object(
            self.bucket, self.get_name(name), data_file, len(data_bytes)
        )
        return self.get_url(name)
