import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey

from app.database import db
from .utils import ModelMixin


class Result(db.Model, ModelMixin):
    __tablename__ = "results"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    variable_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("variables.id")
    )
    categorical: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("result_categorical_options.id")
    )
    population_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("populations.id")
    )
    subpopulation_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("subpopulations.id")
    )

    # Columns
    result: orm.Mapped[str] = orm.mapped_column(sa.Text())
    mean: orm.Mapped[float] = orm.mapped_column()
    sd: orm.Mapped[float] = orm.mapped_column()
    n: orm.Mapped[int] = orm.mapped_column()
    data_string: orm.Mapped[str] = orm.mapped_column(sa.Text())

    def __repr__(self):
        return f"<{self.id}: {self.name}>"


class ResultCategoricalOptions(db.Model, ModelMixin):
    __tablename__ = "result_categorical_options"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Columns
    name: orm.Mapped[str] = orm.mapped_column(sa.Text())
    object_type: orm.Mapped[int] = orm.mapped_column()
    definition: orm.Mapped[str] = orm.mapped_column(sa.Text(), default="")

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
