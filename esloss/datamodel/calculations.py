import enum

from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Enum, Float, String

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import (CompatibleStringArray, CreationInfoMixin,
                                     JSONEncodedDict)


class EStatus(str, enum.Enum):
    PREPARED = 'prepared'
    CREATED = 'created'
    EXECUTING = 'executing'
    COMPLETE = 'complete'
    FAILED = 'failed'
    ABORTED = 'aborted'


class CalculationBranch(ORMBase):
    "Calculation Branch Parameters model"

    config = Column(MutableDict.as_mutable(JSONEncodedDict))
    status = Column(Enum(EStatus), default=EStatus.PREPARED)
    weight = Column(Float())

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'calculationbranch',
        'polymorphic_on': _type,
    }


class RiskCalculationBranch(CalculationBranch):
    __tablename__ = 'loss_riskcalculationbranch'

    _oid = Column(BigInteger, ForeignKey('loss_calculationbranch._oid'),
                  primary_key=True)

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
        backref='riskcalculation',
        foreign_keys=[_occupantsvulnerabilitymodel_oid])

    contentsvulnerabilitymodel = relationship(
        'ContentsVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_contentsvulnerabilitymodel_oid])

    structuralvulnerabilitymodel = relationship(
        'StructuralVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_structuralvulnerabilitymodel_oid])

    nonstructuralvulnerabilitymodel = relationship(
        'NonstructuralVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_nonstructuralvulnerabilitymodel_oid])

    businessinterruptionvulnerabilitymodel = relationship(
        'BusinessInterruptionVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_businessinterruptionvulnerabilitymodel_oid])

    __mapper_args__ = {
        'polymorphic_identity': 'riskcalculationbranch'
    }


class LossCalculation(ORMBase, CreationInfoMixin):
    """Calculation Parameters model"""

    aggregateby = Column(CompatibleStringArray)
    status = Column(Enum(EStatus), default=EStatus.PREPARED)
    description = Column(String())

    _assetcollection_oid = Column(BigInteger,
                                  ForeignKey('loss_assetcollection._oid',
                                             ondelete="RESTRICT"),
                                  nullable=False)
    assetcollection = relationship('AssetCollection',
                                   back_populates='losscalculation')

    _earthquakeinformation_oid = Column(BigInteger, ForeignKey(
        'loss_earthquakeinformation._oid', ondelete='CASCADE'))
    earthquakeinformation = relationship('EarthquakeInformation',
                                         back_populates='losscalculation')

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'losscalculation',
        'polymorphic_on': _type,
    }


class RiskCalculation(LossCalculation):
    __tablename__ = 'loss_riskcalculation'

    _oid = Column(BigInteger, ForeignKey('loss_losscalculation._oid'),
                  primary_key=True)

    losses = relationship('LossValue', back_populates='riskcalculation')

    __mapper_args__ = {
        'polymorphic_identity': 'riskcalculation'
    }


class DamageCalculation(LossCalculation):
    __tablename__ = 'loss_damagecalculation'

    _oid = Column(BigInteger, ForeignKey('loss_losscalculation._oid'),
                  primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'damagecalculation'
    }
