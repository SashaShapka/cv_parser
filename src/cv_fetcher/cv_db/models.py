import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Index
from cv_fetcher.cv_db.allocator import UUID_F
from sqlalchemy.dialects.postgresql import TSVECTOR
Base = declarative_base()


class Candidates(Base):
    __tablename__ = "candidates"

    id = sqlalchemy.Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    skills = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    experience = sqlalchemy.Column(sqlalchemy.String())
    source = sqlalchemy.Column(sqlalchemy.String(), nullable=False, default="dou.ua")
    search_vector = sqlalchemy.Column(TSVECTOR)


    __table_args__ = (
        Index("ix_candidates_name", "name"),
        Index("ix_candidates_skills", "skills"),
        Index("ix_candidates_experience", "experience"),
        Index("ix_candidates_search_vector", "search_vector", postgresql_using="gin"),
    )

    def __init__(self, name, skills, experience):
        self.name = name
        self.skills = skills
        self.experience = experience
