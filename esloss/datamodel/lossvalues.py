import enum

from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, Integer

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import RealQuantityMixin


class ELossCategory(enum.Enum):
    CONTENTS = 'contents'
    BUSINESSINTERRUPTION = 'businessinterruption'
    NONSTRUCTURAL = 'nonstructural'
    OCCUPANTS = 'occupants'
    STRUCTURAL = 'structural'


lossvalue_aggregationtag = Table(
    'loss_assoc_lossvalue_aggregationtag',
    ORMBase.metadata,
    Column('lossvalue', ForeignKey(
        'loss_lossvalue._oid',
        ondelete='CASCADE'),
        primary_key=True),
    Column('aggregationtag', ForeignKey(
        'loss_aggregationtag._oid',
        ondelete='CASCADE'),
        primary_key=True),
)


class LossValue(ORMBase, RealQuantityMixin('loss')):
    '''Loss Value'''

    # id of the realization
    eventid = Column(Integer, nullable=False)
    losscategory = Column(Enum(ELossCategory), nullable=False)
    weight = Column(Float)

    aggregationtags = relationship('AggregationTag',
                                   secondary=lossvalue_aggregationtag,
                                   back_populates='losses',
                                   lazy='joined')

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
