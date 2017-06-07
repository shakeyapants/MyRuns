import click
import MyRuns

with open('VERSION') as version_file:
    version_num = version_file.read().strip()


@click.command(name='MyRuns')
@click.version_option(version_num, '--version', '-V')
@click.option('--setup', '-S', is_flag=True, help='Create database tables.')
def cli(setup):
    if setup:
        with MyRuns.MyRuns.app.app_context():
            MyRuns.MyRuns.db.create_all()
            MyRuns.MyRuns.db.session.commit()
            print('Database tables created')
    else:
        MyRuns.MyRuns.app.run(debug=True, host='0.0.0.0')