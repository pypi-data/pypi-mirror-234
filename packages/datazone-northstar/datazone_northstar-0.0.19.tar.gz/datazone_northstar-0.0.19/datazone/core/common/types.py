from enum import Enum


class SourceType(str, Enum):
    MYSQL = "mysql"
    AWS_S3_CSV = "aws_s3_csv"


class ExtractMode(str, Enum):
    OVERWRITE = "overwrite"
    APPEND = "append"
