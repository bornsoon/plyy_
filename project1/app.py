# app.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'plyy_page'

    from app2 import main, plyy, api_main, api_plyy

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(plyy, url_prefix='/plyy')
    app.register_blueprint(api_main, url_prefix='/api/main')
    app.register_blueprint(api_plyy, url_prefix='/api/plyy')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
