import os
from .cloud import AwsStorage
from .local import LocalDrive
from .network import NetworkDrive

def init_storage(**conf):
    storage = {
        'network': NetworkDrive,
        'aws': AwsStorage,
    }.get(conf['storage_type'], None)

    if storage is None:
        raise Exception('Storage not properly defined in configuration')

    return storage(**conf)


def save_frames(store, conf):
    out_frames = conf.get('out_frames')
    for root, dirs, files in os.walk(out_frames):
        # Process frames
        for frame in files:
            frame_path = os.path.join(root, frame)
            print('saving {}'.format(frame_path))
            #store.save(frame_path, bucket, key)
            store.save(frame_path)
            # Delete saved frame
            print('deleting {}'.format(frame_path))
            os.unlink(frame_path)
