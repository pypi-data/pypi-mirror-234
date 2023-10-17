from __future__ import annotations

import logging
import os
from datetime import datetime, timezone, timedelta

import typer
from celery import Celery
from flask.logging import default_handler
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies
from pydantic_flask import PydanticFlask
from werkzeug.exceptions import HTTPException

from artorias.web.flask.json import JSONProvider
from artorias.web.flask.utils import find_blueprints, find_commands


class Flask(PydanticFlask):
    json_provider_class = JSONProvider

    def __init__(
        self,
        import_name: str,
        static_url_path: str | None = None,
        static_folder: str | os.PathLike | None = "static",
        static_host: str | None = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: str | os.PathLike | None = "templates",
        instance_path: str | None = None,
        instance_relative_config: bool = False,
        root_path: str | None = None,
        settings: dict | None = None,
    ):
        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )

        self.load_settings(settings)
        self.init_logger()
        os.chdir(os.path.dirname(self.root_path))
        self.logger.debug(f"Current work dir: {os.getcwd()}")

        self.load_exts()
        self.load_blueprints()
        self.load_commands()
        self.load_error_handlers()

    def load_exts(self):
        from artorias.web.flask import celery
        from artorias.web.flask.exts import cache, cors, db, migrate, jwt, redis

        db.init_app(self)
        migrate.init_app(self)
        cors.init_app(self)
        cache.init_app(self)
        jwt.init_app(self)

        if self.config.get("CELERY"):
            celery.init_app(self)

        if self.debug:
            with self.app_context():
                db.create_all()

        @self.shell_context_processor
        def make_shell_context():
            return {"cache": cache, "redis": redis}

        if self.config.get("JWT_REFRESH_COOKIE_TOKEN_AFTER_REQUEST"):

            @self.after_request
            def refresh_expiring_jwts(response):
                try:
                    exp_timestamp = get_jwt()["exp"]
                    now = datetime.now(timezone.utc)
                    target_timestamp = datetime.timestamp(
                        now + timedelta(seconds=self.config.get("JWT_REFRESH_COOKIE_TOKEN_BEFORE_EXPIRES"))
                    )
                    if target_timestamp > exp_timestamp:
                        access_token = create_access_token(identity=get_jwt_identity())
                        set_access_cookies(response, access_token)
                    return response
                except (RuntimeError, KeyError):
                    return response

    def load_settings(self, settings: dict | None):
        from artorias.web.flask.settings import DefaultSettings

        default_setttings = DefaultSettings().model_dump()
        if settings:
            default_setttings.update(**settings)
        self.config.from_mapping(default_setttings)

    def load_blueprints(self):
        blueprints_package = f"{os.path.basename(self.root_path)}.apis"
        for blueprint in find_blueprints(blueprints_package):
            self.logger.debug(f"Find blueprint '{blueprint}'")
            self.register_blueprint(blueprint)

    def load_commands(self):
        commands_package = f"{os.path.basename(self.root_path)}.commands"
        for command in find_commands(commands_package):
            click_obj = typer.main.get_command(command)
            self.logger.debug(f"Find command '{click_obj}'")
            self.cli.add_command(click_obj, click_obj.name)

    def init_logger(self):
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        default_handler.setFormatter(logging.Formatter(self.config["LOGGER_FORMAT_STRING"]))
        self.logger.addHandler(default_handler)

    def load_error_handlers(self):
        @self.errorhandler(HTTPException)
        def http_exception(exp: HTTPException):
            return {"msg": exp.description}, exp.code

        @self.errorhandler(Exception)
        def unknown_exception(exp: Exception):
            self.logger.exception(exp)
            return {"msg": self.config["UNKNOWN_EXCEPTION_MESSAGE"]}, 500

    def load_ping_pong(self):
        @self.get("/ping")
        def ping():
            return {"msg": "pong~"}

    @property
    def celery(self) -> Celery | None:
        return self.extensions.get("celery")
