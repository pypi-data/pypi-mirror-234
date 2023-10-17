import functools
from datetime import datetime
from typing import Callable

from artorias.web.flask.exts import db
from sqlalchemy import delete
from sqlalchemy.orm import Mapped, mapped_column


def transaction(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        else:
            return data

    return wrapper


class Model(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        return instance


class PkModel(Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_by_pk(cls, pk: int):
        return db.session.get(cls, pk)

    @classmethod
    def get_or_404(cls, pk: int):
        return db.get_or_404(cls, pk)

    @classmethod
    def delete_by_pk(cls, pk: int):
        return db.session.execute(delete(cls).where(cls.id == pk))


class TimeModel(Model):
    __abstract__ = True

    create_at: Mapped[datetime] = mapped_column(default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
