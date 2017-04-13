import os
from .cloud import AwsStorage
from .local import LocalDrive
from .network import NetworkDrive

def init_storage(**conf):
    storage = {
        'net':   NetworkDrive,
        'aws': AwsStorage,
        'drive': LocalDrive,
    }.get(conf.storage, None)

    if storage is None:
        raise Exception('Storage not properly defined in configuration')


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
