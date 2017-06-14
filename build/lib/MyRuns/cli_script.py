import click
import MyRuns

with open('VERSION') as version_file:
    version_num = version_file.read().strip()


@click.command()
@click.option('--version', '-V', is_flag=True, help='Will print version.')
@click.option('--setup', '-S', is_flag=True, help='Will create database tables.')
def cli(version, setup):
    if version:
        click.echo('MyRuns version {}'.format(version_num))
    elif setup:
        with MyRuns.MyRuns.app.app_context():
            MyRuns.MyRuns.db.create_all()
            MyRuns.MyRuns.db.session.commit()
            print('Database tables created')
    else:
        MyRuns.MyRuns.app.run(debug=True, host='0.0.0.0')