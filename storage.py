import os
import boto3

BLOCK_SIZE = 4096


class Storage:

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
                return response['Body'].read(BLOCK_SIZE)
            for block in iter(read_block, b''):
                destination_file.write(block)


def save_frames(store, bucket, out_frames):
    for root, dirs, files in os.walk(out_frames):
        # Process frames
        for frame in files:
            frame_path = os.path.join(root, frame)
            print('saving {}'.format(frame_path))
            key = frame_path.replace(out_frames, "")
            if key[0] == '/':
                key = key[1:]
            print('using key {}'.format(key))
            store.save(frame_path, bucket, key)
            # Delete saved frame
            print('deleting {}'.format(frame_path))
            os.unlink(frame_path)
