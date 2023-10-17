from artorias.web.flask import Flask


def create_app() -> Flask:
    from $project_name.settings import settings

    app = Flask(__name__, settings=settings.model_dump())
    return app
