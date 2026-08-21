# flaskr/__init__.py
import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    os.makedirs(app.instance_path, exist_ok=True)

    # Registra o blueprint auth
    from . import auth
    app.register_blueprint(auth.bp)

    # Registra o blueprint blog
    from . import blog
    app.register_blueprint(blog.bp)

    from . import db
    db.init_app(app)

    app.add_url_rule('/', endpoint='index')

    return app