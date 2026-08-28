from flask import Flask
from app.extensions import cache, db, limiter, ma
from flask_swagger_ui import get_swaggerui_blueprint
from app.customers import customers_bp
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp
from app.inventory import inventory_bp
from flask_migrate import Migrate

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Shop API Documentation"}
)

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if config_name.startswith("app."):
        config_path = config_name
    elif config_name.startswith("config."):
        config_path = f"app.{config_name}"
    else:
        config_path = f"app.config.{config_name}"
    app.config.from_object(config_path)

    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    return app
