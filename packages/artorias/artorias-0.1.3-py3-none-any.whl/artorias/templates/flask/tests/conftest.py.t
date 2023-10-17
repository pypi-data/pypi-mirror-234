import pytest
from artorias.web.flask import Flask
from artorias.web.flask.exts import db
from flask.testing import FlaskClient

from $project_name import create_app


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
