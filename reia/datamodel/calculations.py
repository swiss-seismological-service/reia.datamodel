import enum

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, String

from reia.datamodel.base import ORMBase
from reia.datamodel.mixins import (CompatibleStringArray, CreationInfoMixin,
                                   JSONEncodedDict)


class EStatus(str, enum.Enum):
    PREPARED = 'prepared'
    CREATED = 'created'
    EXECUTING = 'executing'
    COMPLETE = 'complete'
    FAILED = 'failed'
    ABORTED = 'aborted'


class EEarthquakeType(enum.Enum):
    SCENARIO = 'scenario'
    NATURAL = 'natural'


class ECalculationType(str, enum.Enum):
    RISK = 'risk'
    LOSS = 'loss'
    DAMAGE = 'damage'


class EarthquakeInformation(ORMBase, CreationInfoMixin):
    """Calculation Parameters model"""
    originid = Column(String, nullable=False)
    type = Column(Enum(EEarthquakeType),
                  default=EEarthquakeType.NATURAL,
                  nullable=False)

    calculation = relationship('Calculation',
                               back_populates='earthquakeinformation',
                               passive_deletes=True,
                               cascade='all, delete-orphan')

    __table_args__ = (UniqueConstraint('originid', name='originid_unique'),)


class CalculationBranch(ORMBase):
    """
    Calculation Branch Parameters model

    Instance of SQLAlchemy Joined Table Inheritance
    """

    config = Column(MutableDict.as_mutable(JSONEncodedDict))
    status = Column(Enum(EStatus), default=EStatus.PREPARED)
    weight = Column(Float())

    _exposuremodel_oid = Column(BigInteger,
                                ForeignKey('loss_exposuremodel._oid',
                                           ondelete="RESTRICT"),
                                nullable=False)
    exposuremodel = relationship('ExposureModel',
                                 back_populates='calculationbranch')

    _type = Column(Enum(ECalculationType))

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.RISK,
        'polymorphic_on': _type,
    }


class LossCalculationBranch(CalculationBranch):
    __tablename__ = 'loss_losscalculationbranch'

    _oid = Column(BigInteger, ForeignKey('loss_calculationbranch._oid'),
                  primary_key=True)

    _calculation_oid = Column(BigInteger,
                              ForeignKey('loss_calculation._oid',
                                         ondelete='CASCADE'))
    losscalculation = relationship('LossCalculation',
                                   back_populates='losscalculationbranches')

    losses = relationship('LossValue',
                          back_populates='losscalculationbranch')

    _occupantsvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _contentsvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _structuralvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _nonstructuralvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _businessinterruptionvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))

    occupantsvulnerabilitymodel = relationship(
        'OccupantsVulnerabilityModel',
        backref='losscalculation',
        foreign_keys=[_occupantsvulnerabilitymodel_oid])

    contentsvulnerabilitymodel = relationship(
        'ContentsVulnerabilityModel',
        backref='losscalculation',
        foreign_keys=[_contentsvulnerabilitymodel_oid])

    structuralvulnerabilitymodel = relationship(
        'StructuralVulnerabilityModel',
        backref='losscalculation',
        foreign_keys=[_structuralvulnerabilitymodel_oid])

    nonstructuralvulnerabilitymodel = relationship(
        'NonstructuralVulnerabilityModel',
        backref='losscalculation',
        foreign_keys=[_nonstructuralvulnerabilitymodel_oid])

    businessinterruptionvulnerabilitymodel = relationship(
        'BusinessInterruptionVulnerabilityModel',
        backref='losscalculation',
        foreign_keys=[_businessinterruptionvulnerabilitymodel_oid])

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.LOSS
    }


class DamageCalculationBranch(CalculationBranch):
    __tablename__ = 'loss_damagecalculationbranch'

    _oid = Column(BigInteger, ForeignKey('loss_calculationbranch._oid'),
                  primary_key=True)

    damages = relationship('DamageValue',
                           back_populates='damagecalculationbranch')

    _calculation_oid = Column(BigInteger,
                              ForeignKey('loss_calculation._oid',
                                         ondelete='CASCADE'))
    damagecalculation = relationship('DamageCalculation',
                                     back_populates='damagecalculationbranches')
    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.DAMAGE
    }


class Calculation(ORMBase, CreationInfoMixin):
    """
    Calculation Parameters model

    Instance of SQLAlchemy Single Table Inheritance
    """

    aggregateby = Column(CompatibleStringArray)
    status = Column(Enum(EStatus), default=EStatus.PREPARED)
    description = Column(String())

    _earthquakeinformation_oid = Column(BigInteger, ForeignKey(
        'loss_earthquakeinformation._oid', ondelete='CASCADE'))
    earthquakeinformation = relationship('EarthquakeInformation',
                                         back_populates='calculation')

    _type = Column(Enum(ECalculationType))

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.RISK,
        'polymorphic_on': _type,
    }


class LossCalculation(Calculation):
    __tablename__ = None

    losses = relationship('LossValue',
                          back_populates='losscalculation',
                          passive_deletes=True,
                          cascade='all, delete-orphan')

    losscalculationbranches = relationship('LossCalculationBranch',
                                           back_populates='losscalculation',
                                           passive_deletes=True,
                                           cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.LOSS
    }


class DamageCalculation(Calculation):
    __tablename__ = None

    damages = relationship('DamageValue',
                           back_populates='damagecalculation',
                           passive_deletes=True,
                           cascade='all, delete-orphan')

    damagecalculationbranches = relationship('DamageCalculationBranch',
                                             back_populates='damagecalculation',
                                             passive_deletes=True,
                                             cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': ECalculationType.DAMAGE
    }
