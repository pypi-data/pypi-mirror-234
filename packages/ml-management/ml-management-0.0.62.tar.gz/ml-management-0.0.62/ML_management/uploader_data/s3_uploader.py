"""Define S3Uploader class."""
import os

from boto3 import client
from ML_management.uploader_data.utils import get_space_size, get_upload_paths
from tqdm import tqdm


class S3Uploader:
    """S3 uploader files class."""

    def __init__(self):
        """Init creds."""
        self.default_url = os.environ.get("MLFLOW_S3_ENDPOINT_URL", "http://minio-mlmanagement.ru/")
        self.default_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
        self.default_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin")

    def upload(self, local_path: str, bucket: str, verbose: bool = True):
        """Upload."""
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            raise FileExistsError(f"Path: {local_path} does not exist")

        service_client = client(
            service_name="s3",
            use_ssl=True,
            verify=None,
            endpoint_url=self.default_url,
            aws_access_key_id=self.default_access_key_id,
            aws_secret_access_key=self.default_secret_access_key,
        )
        buckets = [item["Name"] for item in service_client.list_buckets()["Buckets"]]
        if bucket not in buckets:
            service_client.create_bucket(Bucket=bucket)

        space_size = get_space_size(local_path)
        upload_paths = get_upload_paths(local_path)

        with tqdm(
            total=space_size,
            disable=not verbose,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for path in upload_paths:
                with open(path.local_path, "rb") as _file:
                    service_client.upload_fileobj(
                        Fileobj=_file,
                        Bucket=bucket,
                        Key=path.storage_path,
                        Callback=pbar.update,
                    )
