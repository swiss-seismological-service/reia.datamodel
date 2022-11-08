import enum

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import RealQuantityMixin
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, Integer, String


class ELossCategory(enum.Enum):
    CONTENTS = 'contents'
    BUSINESSINTERRUPTION = 'businessinterruption'
    NONSTRUCTURAL = 'nonstructural'
    OCCUPANTS = 'occupants'
    STRUCTURAL = 'structural'


class LossValue(ORMBase, RealQuantityMixin('loss')):
    '''Loss Value'''

    # id of the realization
    eventid = Column(Integer, nullable=False)
    losscategory = Column(Enum(ELossCategory), nullable=False)
    weight = Column(Float)

    _riskcalculation_oid = Column(BigInteger,
                                  ForeignKey('loss_calculation._oid',
                                             ondelete='CASCADE'),
                                  nullable=False)
    riskcalculation = relationship('RiskCalculation',
                                   back_populates='losses')

    _riskcalculationbranch_oid = Column(BigInteger,
                                        ForeignKey(
                                            'loss_riskcalculationbranch._oid',
                                            ondelete='SET NULL'))
    riskcalculationbranch = relationship('RiskCalculationBranch',
                                         back_populates='losses')

    _type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': _type,
        'polymorphic_identity': 'loss',
    }


aggregatedloss_aggregationtag = Table(
    'loss_assoc_aggregatedloss_aggregationtag',
    ORMBase.metadata,
    Column('aggregatedloss', ForeignKey(
        'loss_lossvalue._oid',
        ondelete='CASCADE'),
        primary_key=True),
    Column('aggregationtag', ForeignKey(
        'loss_aggregationtag._oid',
        ondelete='CASCADE'),
        primary_key=True),
)


class AggregatedLoss(LossValue):
    __tablename__ = None
    aggregationtags = relationship('AggregationTag',
                                   secondary=aggregatedloss_aggregationtag,
                                   back_populates='losses',
                                   lazy='joined')
    __mapper_args__ = {
        'polymorphic_identity': 'aggregatedloss'
    }


class SiteLoss(LossValue):
    '''Loss by site'''
    __tablename__ = None

    _site_oid = Column(BigInteger,
                       ForeignKey('loss_site._oid')
                       )
    site = relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'siteloss'
    }
