from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger


class Base(object):

    @ declared_attr
    def __tablename__(cls):
        return f'loss_{cls.__name__.lower()}'

    _oid = Column(BigInteger, primary_key=True)

    def _asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_


ORMBase = declarative_base(cls=Base)
