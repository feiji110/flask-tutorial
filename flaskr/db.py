
"""
The application will use a SQLite database to store users and posts.
Python comes with built-in support for SQLite in the sqlite3 module.
"""

"""
Connect to the Database

The first thing to do when working with a SQLite database(and most
other Python database libraries)is to create a connection to it.
Any queries and operations are performed using the connections,which
is closed after the work is finished.

In web applications this connection is typically tied to the request.
It is created at some point when handling a request, and closed
before the response is sent.
"""
import sqlite3

import click
from flask import current_app,g
from flask.cli import with_appcontext


"""
g is a special object that is unique for each request.It is used
to store data that might be accessed by multiple functions 
during the request.Theconnection is stored and reused instead 
of creating a new connection if get_db is called a second time
in the same request.
"""

"""
current_app is another special object that points to the Flask 
application handling the request.Since you used an application 
factory,there is no application object when writing the rest of
yout code.get_db will be called when the application has been
created and is handling a request, so current_app can be used.
"""
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the exisiting data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)