import argparse
import configparser
from imaging import monitor_loop
from storage.storage import (
    init_storage,
    save_frames,)


def parse_conf(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    bucket = config.get('AWS', 'bucket')
    out_frames = config.get('Frames', 'out_folder')
    aws_keyid = config.get('AWS', 'aws_access_key_id')
    aws_accesskey = config.get('AWS', 'aws_secret_access_key')
    return bucket, out_frames, aws_keyid, aws_accesskey


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default='default.conf',
                        help='Configuration file if different from default')
    parser.add_argument('--img_ext',
                        default='jpg',
                        help='Video frames file extension')
    parser.add_argument('--in_frames',
                        required=True,
                        help='Video frames input folder')

    return parser.parse_args()


def main(args):
    # Initialize
    bucket, out_frames, keyid, access_key = parse_conf(args.config)
    # Setup frame sequence comparison
    conf = {
        'in': args.in_frames,
        'out': out_frames,
        'img_ext': args.img_ext
    }
    monitor_loop.process_frames(conf=conf)
    # Store to AWS
    storage = init_storage(conf)
    save_frames(storage, bucket, out_frames)


if __name__ == '__main__':
    main(parse_args())
