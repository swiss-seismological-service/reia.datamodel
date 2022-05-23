from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Integer, String
from esloss.datamodel.mixins import RealQuantityMixin
from esloss.datamodel.base import ORMBase


class LossValue(ORMBase, RealQuantityMixin('loss')):
    """
        .. note::

        Inheritance is implemented following the `SQLAlchemy Joined Table
        Inheritance
        <https://docs.sqlalchemy.org/en/latest/orm/inheritance.html#joined-table-inheritance>`_
        paradigm.
    """
    _losscalculation_oid = Column(
        BigInteger,
        ForeignKey('loss_losscalculation._oid'),
        nullable=False)
    losscalculation = relationship(
        'LossCalculation',
        back_populates='losses')

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'lossvalue',
        'polymorphic_on': _type,
    }


class MeanAssetLoss(LossValue):
    """Loss by asset"""
    __tablename__ = 'loss_meanassetloss'
    _oid = Column(BigInteger, ForeignKey(
        'loss_lossvalue._oid'), primary_key=True)
    _asset_oid = Column(
        BigInteger,
        ForeignKey('loss_asset._oid'),
        nullable=False)
    asset = relationship('Asset')

    __mapper_args__ = {
        'polymorphic_identity': 'meanassetloss'
    }


class SiteLoss(LossValue):
    """Loss by site"""
    __tablename__ = 'loss_siteloss'
    _oid = Column(BigInteger, ForeignKey(
        'loss_lossvalue._oid'), primary_key=True)
    realizationid = Column(Integer, nullable=False)
    _site_oid = Column(
        BigInteger,
        ForeignKey('loss_site._oid'),
        nullable=False
    )
    site = relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'siteloss'
    }
