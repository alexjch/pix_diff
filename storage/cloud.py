import os
import boto3


class AwsStorage(object):

    BLOCK_SIZE = 4096

    def __init__(self, **kawrgs):
        keyid = kawrgs.get('aws_keyid')
        access_key = kawrgs.get('aws_accesskey')
        bucket = kawrgs.get('bucket')
        key = kawrgs.get('key')
        self.client = boto3.client('s3',
                                   aws_access_key_id=keyid,
                                   aws_secret_access_key=access_key)
        self.bucket = bucket
        self.key = key

    def save(self, source):
        with open(source, 'rb') as content:
            self.client.put_object(ACL='authenticated-read',
                                   Bucket=self.bucket,
                                   Key=self.key + '/' + os.path.basename(source),
                                   Body=content)
            exit()

    def retrieve(self, destination, bucket, key):
        response = self.client.get_object(Bucket=bucket,
                                          Key=key)
        with open(destination, 'wb') as destination_file:
            def read_block():
                return response['Body'].read(self.BLOCK_SIZE)
            for block in iter(read_block, b''):
                destination_file.write(block)
