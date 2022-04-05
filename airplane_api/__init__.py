import os
import click
from logging.config import dictConfig
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def initLog():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s:%(funcName)s() - %(message)s',
        }},
        'handlers': {
            'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
            },
            'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'instance/airplane_api.log',
            'level':'DEBUG'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['file']
        }
    })

def create_app():
    #Configure logging
    initLog()

    #Create app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, app.instance_path,'db.sqlite')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from airplane_api.airplane.models import Airplane

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    from airplane_api import airplane

    app.register_blueprint(airplane.bp)

    return app

def init_db():
    db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")