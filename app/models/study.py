import sqlalchemy as sa
from sqlalchemy import orm, ForeignKey

from app.database import db
from .utils import ModelMixin


class StudyData(db.Model, ModelMixin):
    __tablename__ = "study_data"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    variable_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("variables.id"))
    study_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("studies.id"))
    categorical: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("study_categorical_options.id")
    )

    # Columns
    values: orm.Mapped[str] = orm.mapped_column(sa.Text())

    def __repr__(self):
        return f"<{self.id}: {self.values},{self.categorical.name}>"


class Study(db.Model, ModelMixin):
    __tablename__ = "studies"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Columns
    study: orm.Mapped[str] = orm.mapped_column(sa.Text())

    # Relationships
    study_data: orm.Mapped[StudyData] = orm.relationship()  # TODO should it be a list???
    populations: orm.Mapped[list["Population"]] = orm.relationship()

    def __repr__(self):
        return f"<{self.id}: {self.study}>"


class StudyCategoricalOption(db.Model, ModelMixin):
    __tablename__ = "study_categorical_options"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Columns
    name: orm.Mapped[str] = orm.mapped_column(sa.Text())
    object_type: orm.Mapped[int] = orm.mapped_column()
    definition: orm.Mapped[str] = orm.mapped_column(sa.Text(), default="")

    def __repr__(self):
        return f"<{self.id}: {self.name},{self.object_type}>"

    # @property
    # def json(self):
    #     u = s.User.model_validate(self)
    #     return u.model_dump_json()
