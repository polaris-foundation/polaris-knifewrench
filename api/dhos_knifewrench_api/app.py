from pathlib import Path

import connexion
import kombu_batteries_included
from connexion import FlaskApp
from flask import Flask
from flask_batteries_included import augment_app as fbi_augment_app
from flask_batteries_included.config import is_not_production_environment
from flask_batteries_included.sqldb import init_db
from flask_cors import CORS
from she_logging import logger

from dhos_knifewrench_api.api import api_blueprint
from dhos_knifewrench_api.helper.cli import add_cli_command


def create_app(testing: bool = False) -> Flask:
    # Create a Flask app.
    openapi_dir: Path = Path(__file__).parent / "openapi"
    connexion_app: FlaskApp = connexion.App(
        __name__,
        specification_dir=openapi_dir,
        options={"swagger_ui": is_not_production_environment()},
    )
    connexion_app.add_api("openapi.yaml")
    app: Flask = fbi_augment_app(app=connexion_app.app, use_pgsql=True, testing=testing)
    CORS(app)

    # Register the API blueprint.
    app.register_blueprint(api_blueprint)
    app.logger.info("Registered API blueprint")

    # Configure the SQL database
    init_db(app=app, testing=testing)

    # Initialise k-b-i library to allow publishing to RabbitMQ.
    kombu_batteries_included.init()

    add_cli_command(app)

    # Done!
    logger.info("App ready to serve requests")

    return app
