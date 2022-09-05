"""."""
import os
from flask import Flask, request, g
from flaskr.auth import bp as auth_bp
from flaskr.steno import bp as steno
from flaskr.db import init_db_command
from flaskr.db import init_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(__name__, static_folder='static', template_folder='templates')
application.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/secret"
)
init_app(application)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
application.register_blueprint(auth_bp)
application.register_blueprint(steno)

@application.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return "404 not found", 404

if __name__ == '__main__':
#    init_db_command()
    db.create_all()
    application.run(port=8000, host='0.0.0.0')
