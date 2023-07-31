import boto3
from config import BUCKET, REGION, ACCESS_KEY, SECRET_KEY


def detect_labels(key, max_labels=10, min_confidence=50):
    rekognition = boto3.client("rekognition",
                               region_name=REGION,
                               aws_access_key_id=ACCESS_KEY,
                               aws_secret_access_key=SECRET_KEY)
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": BUCKET,
                "Name": key,
            }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )

    return response['Labels']
