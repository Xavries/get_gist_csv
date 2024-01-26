import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey

from app.database import db
from .utils import ModelMixin


class Subpopulation(db.Model, ModelMixin):
    __tablename__ = "subpopulations"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    population_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("populations.id")
    )

    # Columns
    name: orm.Mapped[str] = orm.mapped_column(sa.Text())
    object_type: orm.Mapped[int] = orm.mapped_column()
    definition: orm.Mapped[str] = orm.mapped_column(sa.Text(), default="")

    def __repr__(self):
        return f"<{self.id}: {self.name},{self.object_type}>"


class SubpopulationData(db.Model, ModelMixin):
    __tablename__ = "subpopulation_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    variable_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("variables.id")
    )
    # NOTE here categorical is a subpopulation_id
    categorical: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("subpopulations.id")
    )

    # Columns
    mean: orm.Mapped[float] = orm.mapped_column()
    sd: orm.Mapped[float] = orm.mapped_column()
    n: orm.Mapped[int] = orm.mapped_column()
    data_string: orm.Mapped[str] = orm.mapped_column(sa.Text())

    def __repr__(self):
        return f"<{self.id}: {self.categorical.name},{self.variable_id.name}>"
