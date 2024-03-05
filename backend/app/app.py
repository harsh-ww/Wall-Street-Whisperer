from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from connect import get_db_connection
import os

def create_app():
    app = Flask(__name__)

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
    from track import track_blueprint
    from api_routes import api_routes_blueprint
    from notifications import notifications_blueprint

    app.register_blueprint(track_blueprint)
    app.register_blueprint(api_routes_blueprint)
    app.register_blueprint(notifications_blueprint)

    return app 

app = create_app()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/example')
def example_database_call():
    try:
        sql_query = "SELECT * FROM company"
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query)

            rows = cur.fetchone()
            print(rows)
    finally:
        conn.close()
        
    return 'Success'


