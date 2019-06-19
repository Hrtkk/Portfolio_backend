import sqlite3
from pymongo import MongoClient
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    db = MongoClient('mongodb://hritik:ZeTtaMiNe@cluster0-shard-00-00-gwkzu.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    return db.zettamine

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# def init_db():
#     db = get_db()

#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """ Clear the existing data and create new tables. """
#     init_db()
#     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
