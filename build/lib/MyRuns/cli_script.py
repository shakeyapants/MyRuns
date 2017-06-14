import click
import MyRuns
from .version import __version__


@click.command(name='MyRuns')
@click.version_option(__version__, '--version', '-V')
@click.option('--setup', '-S', is_flag=True, help='Create database tables.')
def cli(setup):
    if setup:
        with MyRuns.MyRuns.app.app_context():
            MyRuns.MyRuns.db.create_all()
            MyRuns.MyRuns.db.session.commit()
            print('Database tables created')
    else:
        MyRuns.MyRuns.app.run(debug=True, host='0.0.0.0')