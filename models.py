from operator import index
from re import T

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


class templatesinfo(Base):
    __tablename__ = "templatesinfo"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, unique=True, index=True)
    template_words = Column(String, unique=True, index=True)
    keywords = Column(String, index=True)

    def __init__(self, template_name, template_words, keywords):
        self.template_name = template_name
        self.template_words = template_words
        self.keywords = keywords

    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)


class negative_keywords(Base):
    __tablename__ = "negative_keywords"
    id = Column(Integer, primary_key=True, index=True)
    negkeywords = Column(String, unique=True, index=True)

    def __init__(self, negkeywords):
        self.negkeywords = negkeywords
