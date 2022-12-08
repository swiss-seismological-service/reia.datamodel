import enum

from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, Integer, String

from reia.datamodel.base import ORMBase
from reia.datamodel.mixins import RealQuantityMixin


class ELossCategory(enum.Enum):
    CONTENTS = 'contents'
    BUSINESS_INTERRUPTION = 'businessinterruption'
    NONSTRUCTURAL = 'nonstructural'
    OCCUPANTS = 'occupants'
    STRUCTURAL = 'structural'


riskvalue_aggregationtag = Table(
    'loss_assoc_riskvalue_aggregationtag',
    ORMBase.metadata,
    Column('riskvalue', ForeignKey(
        'loss_riskvalue._oid',
        ondelete='CASCADE'),
        primary_key=True),
    Column('aggregationtag', ForeignKey(
        'loss_aggregationtag._oid',
        ondelete='CASCADE'),
        primary_key=True),
    Column('losscategory', ELossCategory),
    Column('_calculation_oid', BigInteger),
    postgresql_partition_by='LIST (_calculation_oid)'
)


class RiskValue(ORMBase):
    __table_args__ = {
        'postgresql_partition_by': 'LIST (_calculation_oid)'
    }
    # id of the realization
    eventid = Column(Integer, nullable=False)
    losscategory = Column(Enum(ELossCategory), nullable=False)
    weight = Column(Float)

    _calculation_oid = Column(BigInteger,
                              ForeignKey('loss_calculation._oid',
                                         ondelete='CASCADE'),
                              nullable=False)
    aggregationtags = relationship('AggregationTag',
                                   secondary=riskvalue_aggregationtag,
                                   back_populates='riskvalues',
                                   lazy='joined')

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'riskvalue',
        'polymorphic_on': _type,
    }


class LossValue(RiskValue, RealQuantityMixin('loss', optional=True)):
    __tablename__ = None

    losscalculation = relationship('LossCalculation',
                                   back_populates='losses')

    _losscalculationbranch_oid = Column(BigInteger,
                                        ForeignKey(
                                            'loss_losscalculationbranch._oid',
                                            ondelete='SET NULL'))
    losscalculationbranch = relationship('LossCalculationBranch',
                                         back_populates='losses')
    __mapper_args__ = {
        'polymorphic_identity': 'lossvalue'
    }


class DamageValue(RiskValue,
                  RealQuantityMixin('dg1', optional=True),
                  RealQuantityMixin('dg2', optional=True),
                  RealQuantityMixin('dg3', optional=True),
                  RealQuantityMixin('dg4', optional=True),
                  RealQuantityMixin('dg5', optional=True)):
    __tablename__ = None

    damagecalculation = relationship('DamageCalculation',
                                     back_populates='damages')

    _damagecalculationbranch_oid = Column(BigInteger, ForeignKey(
        'loss_damagecalculationbranch._oid', ondelete='SET NULL'))
    damagecalculationbranch = relationship('DamageCalculationBranch',
                                           back_populates='damages')
    __mapper_args__ = {
        'polymorphic_identity': 'damagevalue'
    }
