import configparser

STORAGE_TYPES = ['aws', 'network']

def parse_conf(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    storage_type = config.get('Storage', 'type')
    if storage_type not in STORAGE_TYPES:
        print('Storage type {} is unknown'.format(storage_type))
        exit(1)

    kwargs = {
        'storage_type': storage_type,
        'in_frames': config.get('Images', 'in_frames'),
        'out_frames': config.get('Images', 'out_frames'),
        'img_ext': config.get('Images', 'img_ext'),
    }

    if storage_type == 'network':
        kwargs.update({
            'username': config.get('Network', 'username'),
            'password': config.get('Network', 'password'),
            'hostname': config.get('Network', 'hostname'),
            'destination': config.get('Network', 'destination'),
        })
    elif storage_type == 'aws':
        kwargs.update({
            'bucket': config.get('AWS', 'bucket'),
            'aws_keyid': config.get('AWS', 'aws_access_key_id'),
            'aws_accesskey': config.get('AWS', 'aws_secret_access_key'),
            'key': config.get('AWS', 'key'),
        })

    return kwargs




