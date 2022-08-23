import click
import re
import sys
import socket
import string
import unicodedata
import requests
from datetime import datetime
import pytz
import os
from pyicloud.services.photos import PhotoAlbum
from pyicloud import PyiCloudService
from pyicloud.utils import store_password_in_keyring
from pyicloud.exceptions import PyiCloudFailedLoginException, PyiCloudNoStoredPasswordAvailableException
from tqdm import tqdm

BACKUP_FOLDER = os.path.join(os.getcwd(), 'photos')


def clean_filename(filename):
    whitelist=valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:255]

def validate_date(ctx, param, value):
    if not value:
        return value

    if re.match('(1|2)[0-9]{3}-(0|1)[0-9]-[0-3][0-9]', value) == None:
        raise click.BadParameter('Invalid date format, should follow YYYY-MM-DD (ex: 1984-11-23)')
    return pytz.utc.localize(datetime.strptime(value, '%Y-%m-%d')).date()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS, options_metavar='<options>')
@click.option('--username',
              help='Your iCloud username or email address',
              metavar='<username>',
              envvar='USERNAME',
              prompt='iCloud username/email')
@click.option('--from-date',
              help='specifiy a date YYYY-mm-dd to begin downloading images from, leaving it out will result in downloading all images',
              callback=validate_date,
              envvar='FROM_DATE',
              metavar='<date>')
@click.option('--to-date',
              help='Specifiy a date YYYY-mm-dd to begin downloading images to, leaving it out will result in downloading images up till today',
              callback=validate_date,
              envvar='TO_DATE',
              metavar='<date>')

def backup(username, from_date, to_date):
    icloud = authenticate(username)

    album = icloud.photos.all

    # sort by asset-date instead of added-date
    album.obj_type = "CPLAssetByAssetDate"
    album.list_type = "CPLAssetAndMasterByAddedDate"
    album.page_size = 100 # seems to be capped at 100.

    print("Album '{0}' contains a total of {1} photos".format(album.title, len(album)))

    # this could be very memory heavy, to store all photos in-memory instead of using a generator. 
    # to greatly speed up this, we could fork https://github.com/picklepete/pyicloud/blob/master/pyicloud/services/photos.py#L335 to allow us to inject a query-filter to query for photos only within the date range
    # we can reduce the queries needed from O(n) -> O(1) 
    failed_photos = []
    downloaded = 0

    progress_bar = tqdm(total=len(album), desc="Downloading", position=0, bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt}")

    def download_photo(photo):
        nonlocal downloaded
        nonlocal failed_photos
        downloaded += 1

        try:

            if not os.path.exists(photo.download_dir):
                os.makedirs(photo.download_dir)
            
            download_url = photo.download('original')
            # size = photo.size()
            
            if download_url:
                download_bar = tqdm(position=1, unit="byte", desc=photo.download_path, unit_scale=True, bar_format="{l_bar}|{rate_fmt}|{n_fmt}|{elapsed}")
                with open(photo.download_path, 'wb') as file:
                    for chunk in download_url.iter_content(chunk_size=1024):
                        if chunk:
                            download_bar.update(1024)
                            file.write(chunk)
                    file.close()
                download_bar.close()


        except (requests.exceptions.ConnectionError, socket.timeout):
            failed_photos.append(photo)


    # before we can rely heavy on the photos are sorted DESC by asset_date we can create these guards.
    for photo in album.photos:
        progress_bar.update()
        if to_date is not None and photo.created.date() > to_date:
            # skip photos untill photos are older than our 'to_date'
            continue

        if from_date is not None and photo.created.date() < from_date:
            # break out when we begin to receive photos created earlier than our 'from_date'
            break

        date_path = '{:%Y-%m}'.format(photo.created) # store files in folders grouped by year + month.
        photo.download_dir = os.path.join(BACKUP_FOLDER, username, date_path)
        filename = clean_filename(photo.id) + photo.filename.encode('utf-8').decode('ascii', 'ignore')
        photo.download_path = os.path.join(photo.download_dir, filename)
        if os.path.isfile(photo.download_path):
            #skip when we've already fetched the photo
            continue
        
        download_photo(photo)

    progress_bar.close()
    
    print("Finished downloaded {0} of {1} photos, with {2} failed".format(downloaded, len(album), len(failed_photos)))
    
    if failed_photos:
        print("-----------------------------------------------")
        for photo in failed_photos:
            print(" {0}".format(photo.filename))


def authenticate(username):
    """attempt to authenticate user using provided credentials"""
    try:
        api = PyiCloudService(username)
    except (PyiCloudNoStoredPasswordAvailableException, PyiCloudFailedLoginException):
        import click
        password = click.prompt('iCloud Password', hide_input=True)
        store_password_in_keyring(username, password)
        api = PyiCloudService(username)


    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print("  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber'))))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)

    return api


# if __name__ == '__main__':
backup()