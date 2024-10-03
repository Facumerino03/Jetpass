from flask import Flask
import os
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.route import RouteApp
from app.config import config
from app.routes import Route

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    #Cambia el contexto de la aplicación desde test, development y production
    app_context = os.getenv('FLASK_CONTEXT')
    #https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    marshmallow.init_app(app)
    route = RouteApp()
    route.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    route = Route()
    route.init_app(app)
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app