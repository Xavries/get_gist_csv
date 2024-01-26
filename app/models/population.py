import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey

from app.database import db
from .utils import ModelMixin


class Population(db.Model, ModelMixin):
    __tablename__ = "populations"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    study_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("studies.id"))

    # Columns
    population: orm.Mapped[str] = orm.mapped_column(sa.Text())
    longitudinal: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        default=False
    )  # TODO: DEFAULT FALSE???

    def __repr__(self):
        return f"<{self.id}: {self.population},{self.study.name}>"


class PopulationCategoricalOption(db.Model, ModelMixin):
    __tablename__ = "population_categorical_options"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Columns
    name: orm.Mapped[str] = orm.mapped_column(sa.Text())
    object_type: orm.Mapped[int] = orm.mapped_column()
    definition: orm.Mapped[str] = orm.mapped_column(sa.Text(), default="")

    def __repr__(self):
        return f"<{self.id}: {self.name},{self.object_type}>"


class PopulationData(db.Model, ModelMixin):
    __tablename__ = "population_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    variable_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("variables.id")
    )
    population_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("populations.id")
    )
    categorical: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("population_categorical_options.id")
    )

    # Columns
    mean: orm.Mapped[float] = orm.mapped_column()
    sd: orm.Mapped[float] = orm.mapped_column()
    median: orm.Mapped[float] = orm.mapped_column()
    p25: orm.Mapped[float] = orm.mapped_column()
    p75: orm.Mapped[float] = orm.mapped_column()
    n: orm.Mapped[int] = orm.mapped_column()

    def __repr__(self):
        return f"<{self.id}: {self.categorical.name},{self.variable_id.name}>"
