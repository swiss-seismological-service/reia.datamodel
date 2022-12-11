import enum

from sqlalchemy import ForeignKeyConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, Integer, String

from reia.datamodel.base import ORMBase
from reia.datamodel.calculations import ECalculationType
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

    Column('riskvalue', BigInteger),
    Column('risktype', Enum(ECalculationType)),
    Column('_calculation_oid', ForeignKey('loss_calculation._oid',
                                          ondelete='SET NULL')),

    Column('aggregationname', String),
    Column('aggregationtype', String),

    ForeignKeyConstraint(['riskvalue', 'risktype', '_calculation_oid'],
                         ['loss_riskvalue._oid', 'loss_riskvalue._type',
                          'loss_riskvalue._calculation_oid'],
                         ondelete='CASCADE'),

    ForeignKeyConstraint(['aggregationname', 'aggregationtype'],
                         ['loss_aggregationtag.name',
                         'loss_aggregationtag.type'],
                         ondelete='CASCADE'),

    postgresql_partition_by='LIST (_calculation_oid)'
)


class RiskValue(ORMBase):
    _oid = Column(BigInteger, autoincrement=True,
                  primary_key=True)
    _type = Column(Enum(ECalculationType),
                   primary_key=True)

    losscategory = Column(Enum(ELossCategory))
    eventid = Column(Integer)  # id of the realization
    weight = Column(Float)

    _calculation_oid = Column(BigInteger,
                              ForeignKey('loss_calculation._oid',
                                         ondelete='CASCADE'),
                              primary_key=True)

    aggregationtags = relationship('AggregationTag',
                                   secondary=riskvalue_aggregationtag,
                                   back_populates='riskvalues',
                                   lazy='joined')

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.RISK,
        'polymorphic_on': _type,
    }
    __table_args__ = {
        'postgresql_partition_by': 'LIST (_calculation_oid)',
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
        'polymorphic_identity': ECalculationType.LOSS
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
        'polymorphic_identity': ECalculationType.DAMAGE
    }
