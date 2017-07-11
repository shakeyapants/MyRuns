import click
import MyRuns
import os
import yaml
import platform
from pathlib import Path
from .version import __version__


place = os.path.dirname(os.path.abspath(__file__))

# folder for files
PROJECT_NAME = 'MyRuns'


# finding directory for project files
if platform.uname().system == 'Windows':
    home = str(Path("%s/%s" % (os.getenv('LOCALAPPDATA'), PROJECT_NAME)))
elif platform.uname().system == 'Linux' or 'Darwin':
    home = str(Path("%s/%s" % (os.getenv('HOME'), PROJECT_NAME)))

# create home directory
try:
    os.mkdir(home)
except FileExistsError:
    pass


@click.group()
@click.version_option(__version__, '--version', '-V')
def cli():
    pass


@click.command()
def run():
    MyRuns.MyRuns.app.run(host='0.0.0.0')


@click.command()
@click.option('--MY_STRAVA_CLIENT_ID', prompt='Your strava client ID')
@click.option('--MY_STRAVA_SECRET', prompt='Your strava secret')
@click.option('--REDIRECT_URI', prompt='Your redirect URI')
@click.option('--SECRET_KEY', prompt='Your secret key')
def config(my_strava_client_id, my_strava_secret, redirect_uri, secret_key):
    with open(os.path.join(home, 'config.yaml'), 'w') as f:
        yaml.dump(({'MY_STRAVA_CLIENT_ID': my_strava_client_id,
                    'MY_STRAVA_SECRET': my_strava_secret,
                    'REDIRECT_URI': redirect_uri,
                    'SECRET_KEY': secret_key}), f)
    click.echo('config created')


@click.command()
def database():
    open(os.path.join(home, 'user_token.db'), 'a').close()
    with open(os.path.join(home, 'db_address.yaml'), 'w') as f:
        yaml.dump(({'DB_ADDRESS': 'sqlite:///{}/user_token.db'.format(home)}), f)
    click.echo('database file created')


@click.command()
def setup():
    with MyRuns.MyRuns.app.app_context():
        MyRuns.MyRuns.db.create_all()
        MyRuns.MyRuns.db.session.commit()
        print('Database tables created')


cli.add_command(run)
cli.add_command(config)
cli.add_command(database)
cli.add_command(setup)
