from flask import Flask

from app.extensions import bcrypt, db, migrate, jwt
from app.routes import auth_bp, users_bp, products_bp, orders_bp

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    return app