from flask import Flask
from flask import request
from flask import g
import os
from flaskr.auth import bp as auth_bp
from flaskr.blog import bp as blog_bp
from flaskr.db import init_db_command


application = Flask(__name__)
application.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
)
application.register_blueprint(auth_bp)
application.register_blueprint(blog_bp)

@application.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return "404 not found", 404

if __name__ == '__main__':
    # init_db_command()
    application.run(port=8000, host='0.0.0.0')
