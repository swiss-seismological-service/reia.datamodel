import enum

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import RealQuantityMixin
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Integer, String


class ELossCategory(enum.Enum):
    CONTENTS = 0
    BUSINESSINTERRUPTION = 1
    NONSTRUCTURAL = 2
    OCCUPANTS = 3
    STRUCTURAL = 4


class LossValue(ORMBase, RealQuantityMixin('loss')):
    '''Loss Value'''

    # id of the realization
    eventid = Column(Integer, nullable=False)
    losscategory = Column(Enum(ELossCategory), nullable=False)

    _losscalculation_oid = Column(
        BigInteger,
        ForeignKey('loss_riskcalculation._oid'),
        nullable=False)
    riskcalculation = relationship(
        'RiskCalculation',
        back_populates='losses')

    _type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': _type,
        'polymorphic_identity': 'loss',
    }


aggregatedloss_aggregationtag = Table(
    'loss_aggregatedloss_aggregationtag',
    ORMBase.metadata,
    Column('aggregatedloss', ForeignKey(
        'loss_lossvalue._oid',
        onupdate='CASCADE',
        ondelete='CASCADE'),
        primary_key=True),
    Column('aggregationtag', ForeignKey(
        'loss_aggregationtag._oid',
        onupdate='CASCADE',
        ondelete='CASCADE'),
        primary_key=True),
)


class AggregatedLoss(LossValue):
    __tablename__ = None
    aggregationtags = relationship(
        'AggregationTag',
        secondary=aggregatedloss_aggregationtag,
        back_populates='losses',
        lazy='joined')
    __mapper_args__ = {
        'polymorphic_identity': 'aggregatedloss'
    }


class SiteLoss(LossValue):
    '''Loss by site'''
    __tablename__ = None

    _site_oid = Column(
        BigInteger,
        ForeignKey('loss_site._oid')
    )
    site = relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'siteloss'
    }
