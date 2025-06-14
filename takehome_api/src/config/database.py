from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    def __init__(self):
        super().__init__()
        self.app = None

    def init_db(self, app):
        self.init_app(app)
        with app.app_context():
            self.create_all()


db = Database()
