import enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Integer, String, Enum
from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import RealQuantityMixin


class ELossCategory(enum.Enum):
    contents = 0
    businessinterruption = 1
    nonstructural = 2
    occupants = 3
    structural = 4


class LossValue(ORMBase, RealQuantityMixin('loss')):
    """Loss Value"""

    # id of the realization
    eventid = Column(Integer, nullable=False)
    losscategory = Column(Enum(ELossCategory), nullable=False)

    _losscalculation_oid = Column(
        BigInteger,
        ForeignKey('loss_losscalculation._oid'),
        nullable=False)
    losscalculation = relationship(
        'LossCalculation',
        back_populates='losses')

    _type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': _type,
        'polymorphic_identity': 'loss',
    }


class AggregatedLoss(LossValue):
    __tablename__ = None
    _aggregationtag_oid = Column(BigInteger,
                                 ForeignKey('loss_aggregationtag._oid'),
                                 nullable=False)
    aggregationtag = relationship('AggregationTag')
    __mapper_args__ = {
        'polymorphic_identity': 'aggregatedloss'
    }


class SiteLoss(LossValue):
    """Loss by site"""
    __tablename__ = None

    _site_oid = Column(
        BigInteger,
        ForeignKey('loss_site._oid'),
        nullable=False
    )
    site = relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'siteloss'
    }
