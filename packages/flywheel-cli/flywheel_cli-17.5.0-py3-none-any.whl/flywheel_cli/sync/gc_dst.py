from google.cloud import storage

CHUNKSIZE = 8 << 20  # 8 MB


class GCDestination:
    def __init__(self, bucket, prefix):
        self.bucket_name = bucket
        self.prefix = prefix
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def check_perms(self):
        temp_file = f"{self.prefix}/permcheck.txt"
        try:
            blob = self.bucket.blob(temp_file)
            blob.upload_from_string("")
            if blob.exists():
                blob.delete()
                return True
        except Exception as e:  # pylint: disable=broad-except
            print(f"Permission Error: {e}")
            return False
        return False

    def file(self, relpath):
        return GCFile(
            bucket_name=self.bucket_name,
            relpath=relpath,
            client=self.client,
        )

    def __iter__(self):
        blobs = self.client.list_blobs(self.bucket_name, prefix=self.prefix)
        return (self.file(blob) for blob in blobs)


class GCFile:
    def __init__(self, bucket_name, relpath, client):
        self.client = client
        self.size = None
        self.modified = None
        self.name = None
        self.bucket = self.client.get_bucket(bucket_name)
        self.blob = self.bucket.blob(relpath)
        self.filepath = relpath

    def stat(self):
        try:
            self.blob.reload()
            self.size = self.blob.size
            self.modified = self.blob.updated.timestamp()
            self.name = self.blob.name
            return {
                "name": self.blob.name,
                "size": self.blob.size,
                "content_type": self.blob.content_type,
                "time_created": self.blob.time_created,
                "time_updated": self.blob.updated,  #
            }
        except Exception:  # pylint: disable=broad-except
            return {}

    def store(self, file_obj):
        with self.blob.open(mode="wb") as blob_out:
            while True:
                data = file_obj.read(CHUNKSIZE)
                if not data:
                    break
                blob_out.write(data)
