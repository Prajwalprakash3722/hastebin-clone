import click
from flask.cli import with_appcontext

from .app import db, Code


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    """Create the database tables."""
    db.create_all()
    click.echo('Created the database tables.')
