import click
import re
import sys
import socket
import string
import unicodedata
import requests
import time
from datetime import datetime
import pytz
import os
from pyicloud.services.photos import PhotoAlbum
from pyicloud import PyiCloudService
from tqdm import tqdm
import concurrent.futures

# For retrying connection after timeouts and errors
MAX_CONCURRENT_DOWNLOADS = 8
MAX_RETRIES = 3
WAIT_SECONDS = 5
BACKUP_FOLDER = os.path.join(os.getcwd(), 'backup')


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
    icloud = PyiCloudService(username)

    album = icloud.photos.albums["All Photos"]

    # sort by asset-date instead of added-date
    album.obj_type = "CPLAssetByAssetDate"
    album.list_type = "CPLAssetAndMasterByAddedDate"
    album.page_size = 100 # seems to be capped at 100.

    print("Album '{0}' contains a total of {1} photos".format(album.title, len(album)))

    # this could be very memory heavy, to store all photos in-memory instead of using a generator. 
    # to greatly speed up this, we could fork https://github.com/picklepete/pyicloud/blob/master/pyicloud/services/photos.py#L335 to allow us to inject a query-filter to query for photos only within the date range
    # we can reduce the queries needed from O(n) -> O(1) 
    filtered_photos = []

    photo_filter_bar = tqdm(total=len(album), unit="photos", desc="Filter")

    # before we can rely heavy on the photos are sorted DESC by asset_date we can create these guards.
    for photo in album.photos:
        photo_filter_bar.update()
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

        filtered_photos.append(photo)
        # print("id: {0}, name: {1} created: {2}, added: {3}, path: {4}".format(photo.id, photo.filename, photo.created, photo.added_date, photo.download_path))

    photo_filter_bar.close()
    print("Finished filtering photos, will begin to download {0} photos".format(len(filtered_photos)))
    
    progress_bar = tqdm(total=len(filtered_photos), desc="Downloading", bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt}")
    failed_photos = []

    def download_photo(photo):

        for attempt in range(MAX_RETRIES):
            try:

                if not os.path.exists(photo.download_dir):
                    os.makedirs(photo.download_dir)
                
                download_url = photo.download('original')
                
                if download_url:
                    with open(photo.download_path, 'wb') as file:
                        for chunk in download_url.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)

                break

            except (requests.exceptions.ConnectionError, socket.timeout):
                if (attempt + 1) == MAX_RETRIES:
                    failed_photos.append(photo)
                time.sleep(WAIT_SECONDS)

        progress_bar.update(1)


    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
        futures = {executor.submit(download_photo, photo) for photo in filtered_photos}
        concurrent.futures.wait(futures)

    progress_bar.close()
    
    print("Finished downloaded {0} photos, with {1} failed".format(len(filtered_photos), len(failed_photos)))
    
    if failed_photos:
        print("-----------------------------------------------")
        for photo in failed_photos:
            print(" {0}".format(photo.filename))


if __name__ == '__main__':
    backup()