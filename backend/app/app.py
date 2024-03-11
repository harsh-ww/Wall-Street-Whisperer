from flask import Flask
from flask_cors import CORS
from psycopg2 import DatabaseError
import os
import logging

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Configuration of flask mail
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'stockapp220@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEBUG'] = True
    app.config['MAIL_DEFAULT_SENDER'] = ('no-reply', "no-reply@stockapp.com")

    # Register blueprints
    from routes.track_routes import track_blueprint
    from routes.company_routes import company_routes_blueprint
    from routes.article_routes import article_routes_blueprint
    from notifications import notifications_blueprint
    from emails import emails_blueprint

    app.register_blueprint(track_blueprint)
    app.register_blueprint(company_routes_blueprint)
    app.register_blueprint(notifications_blueprint)
    app.register_blueprint(article_routes_blueprint)
    app.register_blueprint(emails_blueprint)

    return app 

app = create_app()

@app.errorhandler(DatabaseError)
def handle_db_error(err):
    logging.error(err)
    print(err)
    return 'Database Error', 500
