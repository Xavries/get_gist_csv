import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class Variable(db.Model, ModelMixin):
    __tablename__ = "variables"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Columns
    name: orm.Mapped[str] = orm.mapped_column(sa.Text())
    default: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    definition: orm.Mapped[str] = orm.mapped_column(sa.Text(), default="")
    # TODO: try enum for var_type in gist
    var_type: orm.Mapped[str] = orm.mapped_column(sa.String(32), default="")

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
