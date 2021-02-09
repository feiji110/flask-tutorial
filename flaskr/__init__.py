"""
The __init__.py serves double duty:it will contain the
application factory, and it tells Python that the flaskr
directory should be treated as package.
"""
import os

from flask import Flask

def create_app(test_config=None):
    """
    create_app is the application factory function.You'll add
    to it later in the tutorial,but it already does a lot.
    """

    #cteate and configure the app
    app = Flask(__name__, instance_relative_config=True)
        #creates the Flask
        #__name__ is the name of the current Python module.The app needs to know where it's located to set up some paths, and __name__ is a convenient way to tell it that.
        # instance_relative_config=True tells the app that configuration files are relative to the instance folder.The instance folder is located outside the flaskr package and hold local data that shouldn't be committed to veersion control,such as configuration secrets and the database file.


    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
        )
        # set some default configuration that the app will use:
            # SECRET_KEY is used to by Flask and extensions to keep data safe.It's set to 'dev' to provide a convenient value during development, but it should be overridden with a random value when deploying
    if test_config is None:
        #load the instance config,if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'hello, world!'

    from . import db
    db.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)
    return app




