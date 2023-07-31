from PIL import Image
from io import BytesIO
import numpy as np
import boto3
from config import BUCKET, REGION, ACCESS_KEY, SECRET_KEY


def get_image_from_s3(key):
    s3 = boto3.resource('s3',
                        region_name=REGION,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)

    bucket = s3.Bucket(BUCKET)
    object = bucket.Object(key)
    response = object.get()['Body'].read()

    return response


# DEPRECIATED
def read_image_from_s3(bucket, key, region_name=REGION):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3
    region_name: basestring
    region s3

    Returns
    -------
    np array
        Image array
    """
    s3 = boto3.resource('s3', region_name='ap-southeast-1')
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)


def write_image_to_s3(img_array, bucket, key, region_name=REGION):
    """Write an image array into S3 bucket

    Parameters
    ----------
    img_array: string
        Image String Array
    bucket: string
        bucket
    key : string
        Path in s3
    region_name: basestring
        region s3

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3', region_name, aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
    bucket = s3.Bucket(BUCKET)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im = Image.fromarray(img_array)
    im.save(file_stream, format='jpeg')
    object.put(Body=file_stream.getvalue())


def upload_image_to_s3(image, key, region_name=REGION):
    s3 = boto3.resource('s3', region_name, aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
    bucket = s3.Bucket(BUCKET)
    object = bucket.Object(key)
    object.put(Body=image)
