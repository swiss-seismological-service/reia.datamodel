from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, String
from esloss.datamodel.mixins import CreationInfoMixin
from esloss.datamodel.base import ORMBase


class LossCalculation(ORMBase, CreationInfoMixin):
    """Calculation Parameters model"""
    aggregateBy = Column(String(20))

    _assetcollection_oid = Column(BigInteger,
                                  ForeignKey('loss_assetcollection._oid',
                                             ondelete="RESTRICT"),
                                  nullable=False)
    assetcollection = relationship('AssetCollection',
                                   back_populates='losscalculation')

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'losscalculation',
        'polymorphic_on': _type,
    }


class RiskCalculation(LossCalculation):
    __tablename__ = 'loss_riskcalculation'
    _oid = Column(BigInteger,
                  ForeignKey('loss_losscalculation._oid'),
                  primary_key=True)

    # occupancevulnerabilitymodel = relationship(
    #     'OccupanceVulnerabilityModel',
    #     back_populates='riskcalculation_occupance')
    # _occupancevulnerabilitymodel_oid = Column(
    #     BigInteger,
    #     ForeignKey('loss_occupancevulnerabilitymodel._oid',
    #                ondelete='RESTRICT'),
    #     nullable=False)

    # _vulnerabilitymodel_occupance_oid = Column(
    #     BigInteger,
    #     ForeignKey('loss_vulnerabilitymodel._oid',
    #                ondelete='RESTRICT'),
    #     nullable=False)

    # vulnerabilitymodel_occupance = relationship(
    #     'VulnerabilityModel', foreign_keys=[_vulnerabilitymodel_occupance_oid])

    __mapper_args__ = {
        'polymorphic_identity': 'riskcalculation'
    }
