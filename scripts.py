from subprocess import check_call
from dotenv import load_dotenv
import os
from takehome_api.src.main import create_app
from tests.populate_db import populate_database
from tests.query_db import query_db


def server() -> None:
    """Run the Flask server"""
    check_call(["python", "app.py"])


def populate() -> None:
    """DESTROYS and initializes the database with sample data"""
    load_dotenv(verbose=True)

    config_name = os.getenv("APP_SETTING", "development")
    app = create_app(config_name)

    with app.app_context():
        populate_database()


def query() -> None:
    """Queries the database and returns a readable json"""
    load_dotenv(verbose=True)

    config_name = os.getenv("APP_SETTING", "development")
    app = create_app(config_name)

    with app.app_context():
        query_db()
