import argparse
from config import parse_conf
from imaging import monitor_loop
from storage.storage import (
    init_storage,
    save_frames,)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default='default.conf',
                        help='Configuration file if different from default')
    return parser.parse_args()


def main(args):
    # Initialize
    # bucket, out_frames, keyid, access_key = parse_conf(args.config)
    conf = parse_conf(args.config)
    # Setup frame sequence comparison
    monitor_loop.process_frames(conf=conf)
    # Store frames
    storage = init_storage(**conf)
    save_frames(storage, conf)


if __name__ == '__main__':
    main(parse_args())
