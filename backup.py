import click
import re
from pyicloud import PyiCloudService

def validate_date(ctx, param, value):
    if re.match('(1|2)[0-9]{3}-(0|1)[0-9]-[0-3][0-9]', value) == None:
        raise click.BadParameter('Invalid date format, should follow YYYY-MM-DD (ex: 1984-11-23)')
    return value

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
def backup(username, password):
    auth(username, password)

def auth(username, password):
    icloud = PyiCloudService(username, password)
    print(icloud.requires_2fa)


if __name__ == '__main__':
    backup()
