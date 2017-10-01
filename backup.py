import click
import re
import sys
import socket
import requests
import time
from datetime import datetime
import pytz
import os
from pyicloud import PyiCloudService

# For retrying connection after timeouts and errors
MAX_RETRIES = 5
WAIT_SECONDS = 5
BACKUP_FOLDER = os.path.join(os.getcwd(), 'backup')

def validate_date(ctx, param, value):
    if not value:
        return value

    if re.match('(1|2)[0-9]{3}-(0|1)[0-9]-[0-3][0-9]', value) == None:
        raise click.BadParameter('Invalid date format, should follow YYYY-MM-DD (ex: 1984-11-23)')
    return pytz.utc.localize(datetime.strptime(value, '%Y-%m-%d'))

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS, options_metavar='<options>')
@click.option('--username',
              help='Your iCloud username or email address',
              metavar='<username>',
              prompt='iCloud username/email')
@click.option('--password',
              help='Your iCloud password',
              metavar='<password>',
              prompt='iCloud password',
              hide_input=True)
@click.option('--from-date',
              help='specifiy a date YYYY-mm-dd to begin downloading images from',
              callback=validate_date,
              metavar='<date>')
@click.option('--to-date',
              help='Specifiy a date YYYY-mm-dd to begin downloading images to',
              callback=validate_date,
              metavar='<date>')
def backup(username, password, from_date, to_date):
    icloud = authenticate(username, password)

    print("Looking up all photos...")

    all_photos = icloud.photos.all
    
    print("Found (%s) total photos" % (len(all_photos)))

    if from_date is None and to_date is None:
        if not click.confirm("No date filtered specified, will download all photos?"):
            return

    for photo in all_photos:
        for _ in range(MAX_RETRIES):
            try:
                if (from_date is not None and photo.created < from_date) or (to_date is not None and photo.created > to_date):
                    print("skipped", photo.created)
                    continue

                date_path = '{:%Y-%m}'.format(photo.created) # store files in folders grouped by year + month.
                download_dir = os.path.join(BACKUP_FOLDER, date_path)
                
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                
                filename = photo.filename.encode('utf-8').decode('ascii', 'ignore')
                download_path = os.path.join(download_dir, filename)

                download_url = photo.download('original')

                if download_url:
                    with open(download_path, 'wb') as file:
                        for chunk in download_url.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                
                print("downloaded %s" % (download_url))

                return

            except (requests.exceptions.ConnectionError, socket.timeout):
                time.sleep(WAIT_SECONDS)
    return

def authenticate(username, password):
    """attempt to authenticate user using provided credentials"""

    icloud = PyiCloudService(username, password)

    if icloud.requires_2sa:
        print "Two-factor authentication required. Your trusted devices are:"

        devices = icloud.trusted_devices
        for i, device in enumerate(devices):
            print "  %s: %s" % (i, device.get('deviceName', "SMS to %s" % device.get('phoneNumber')))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not icloud.send_verification_code(device):
            print "Failed to send verification code"
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not icloud.validate_verification_code(device, code):
            print "Failed to verify verification code"
            sys.exit(1)

    return icloud


if __name__ == '__main__':
    backup()
