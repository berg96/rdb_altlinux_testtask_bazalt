from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base, declared_attr


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Package:
    name = Column(String(200))
    epoch = Column(Integer)
    version = Column(String(200))
    release = Column(String(200))
    arch = Column(String(200))
    disttag = Column(String(200))
    buildtime = Column(Integer)
    source = Column(String(200))

    def __repr__(self):
        return f'{self.__class__.__name__} {self.name} {self.version} {self.arch}'

    class Meta:
        abstract = True


class FirstLib(Base, Package):
    pass


class SecondLib(Base, Package):
    pass
