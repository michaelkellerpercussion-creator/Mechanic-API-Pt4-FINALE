from flask import Blueprint
from app.service_tickets import routes
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

CORS(app)

service_tickets_bp = Blueprint('service_tickets_bp', __name__)

