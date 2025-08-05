from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Superhero(Base):
    __tablename__ = "superheroes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    intelligence: Mapped[int] = mapped_column(default=0)
    strength: Mapped[int] = mapped_column(default=0)
    speed: Mapped[int] = mapped_column(default=0)
    durability: Mapped[int] = mapped_column(default=0)
    power: Mapped[int] = mapped_column(default=0)
    combat: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"Superhero(id={self.id}, name={self.name})"

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
