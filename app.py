#Flask
from flask import Flask

from config import DevelopmentConfig
from extensions import bcrypt, db, migrate, jwt

from routes import auth_bp, users_bp, products_bp, orders_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

if __name__ == '__main__':
    app.run(debug=True)