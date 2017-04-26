
import os
import subprocess

CMD = "{root_dir}/deploy -dst {destination} -host {host} -src {source} -user {user} -passwd {password}"

class NetworkDrive():

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.hostname = kwargs.get('hostname')
        self.destination = kwargs.get('destination')

    def save(self, source):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = CMD.format(**{
            'root_dir': root_dir,
            'source': source,
            'destination': os.path.join(self.destination, os.path.basename(source)),
            'host': self.hostname,
            'user': self.username,
            'password': self.password,
        }).split(" ")
        return subprocess.run(cmd)


if __name__ == '__main__':
    drive = NetworkDrive(**{
        'user': '<USER>',
        'password': '<PASSWD>',
        'host': '<HOST_or_IP>'})
    r = drive.save('/Users/alexjch/Downloads/start_qemu.sh', 'start_qemu.sh')
    exit(r.returncode)