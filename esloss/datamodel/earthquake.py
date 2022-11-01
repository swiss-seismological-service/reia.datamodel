import enum

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Enum, Float, Integer, String

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import CreationInfoMixin, RealQuantityMixin


class EEarthquakeType(enum.Enum):
    SCENARIO = 'scenario'
    NATURAL = 'natural'


class EarthquakeInformation(
        ORMBase,
        CreationInfoMixin,
        RealQuantityMixin('depth'),
        RealQuantityMixin('latitude'),
        RealQuantityMixin('longitude')):
    """Calculation Parameters model"""

    time = Column(DateTime())
    eventid = Column(String(), nullable=False)
    magnitude = Column(Float())
    evaluationmethod = Column(String())
    hazardlevel = Column(Integer())
    type = Column(Enum(EEarthquakeType),
                  default=EEarthquakeType.NATURAL,
                  nullable=False)

    calculation = relationship('Calculation',
                               back_populates='earthquakeinformation',
                               passive_deletes=True,
                               cascade='all, delete-orphan')

    __table_args__ = (UniqueConstraint('eventid', name='eventid_unique'),)
