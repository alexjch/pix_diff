import boto3


class AwsStorage(object):

    BLOCK_SIZE = 4096

    def __init__(self, keyid, access_key):
        self.client = boto3.client('s3',
                                   aws_access_key_id=keyid,
                                   aws_secret_access_key=access_key)

    def save(self, source, bucket, key):
        with open(source, 'rb') as content:
            self.client.put_object(ACL='authenticated-read',
                                   Bucket=bucket,
                                   Key=key,
                                   Body=content)

    def retrieve(self, destination, bucket, key):
        response = self.client.get_object(Bucket=bucket,
                                          Key=key)
        with open(destination, 'wb') as destination_file:
            def read_block():
                return response['Body'].read(self.BLOCK_SIZE)
            for block in iter(read_block, b''):
                destination_file.write(block)
