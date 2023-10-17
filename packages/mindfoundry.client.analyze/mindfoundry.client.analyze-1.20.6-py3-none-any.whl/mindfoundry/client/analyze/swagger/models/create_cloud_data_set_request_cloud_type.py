from enum import Enum


class CreateCloudDataSetRequestCloudType(str, Enum):
    AWS_S3 = "aws-s3"
    GCP_GCS = "gcp-gcs"

    def __str__(self) -> str:
        return str(self.value)