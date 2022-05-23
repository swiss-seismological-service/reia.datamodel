from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import (ClassificationMixin, CreationInfoMixin,
                                     PublicIdMixin, RealQuantityMixin)


class AssetCollection(ORMBase, PublicIdMixin, CreationInfoMixin):
    """Asset Collection model"""
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    taxonomysource = Column(String)
    occupancyperiods = Column(ARRAY(String))

    costtype = relationship('CostType', back_populates='assetcollection',
                            passive_deletes=True,
                            cascade='all, delete-orphan',
                            lazy='joined')

    losscalculation = relationship('LossModel',
                                   back_populates='assetcollection')

    assets = relationship('Asset',
                          back_populates='assetcollection',
                          passive_deletes=True,
                          cascade='all, delete-orphan')
    sites = relationship('Site',
                         back_populates='assetcollection',
                         passive_deletes=True,
                         cascade='all, delete-orphan')


class CostType(ORMBase):
    name = Column(String)
    type = Column(String)
    unit = Column(String)

    _assetcollection_oid = Column(BigInteger, ForeignKey(
        'loss_assetcollection._oid', ondelete='CASCADE'))
    assetcollection = relationship(
        'AssetCollection',
        back_populates='costtype')


class Asset(PublicIdMixin,
            ClassificationMixin('taxonomy'),
            RealQuantityMixin('contentsvalue'),
            RealQuantityMixin('structuralvalue'),
            RealQuantityMixin('dayoccupancy'),
            RealQuantityMixin('nightoccupancy'),
            RealQuantityMixin('transitoccupancy'),
            RealQuantityMixin('nonstructuralvalue'),
            RealQuantityMixin('businessinterruptionvalue'),
            ORMBase):
    """Asset model"""

    buildingcount = Column(Integer, nullable=False)

    _assetcollection_oid = Column(BigInteger,
                                  ForeignKey('loss_assetcollection._oid',
                                             ondelete="CASCADE"))
    assetcollection = relationship('AssetCollection',
                                   back_populates='assets')

    # site relationship
    _site_oid = Column(BigInteger,
                       ForeignKey('loss_site._oid'),
                       nullable=False)
    site = relationship('Site',
                        back_populates='assets',
                        lazy='joined')

    @classmethod
    def get_keys(cls):
        return cls.__table__.c.keys()


class Site(PublicIdMixin,
           RealQuantityMixin('latitude'),
           RealQuantityMixin('longitude'),
           ORMBase):
    """Site model"""

    # asset collection relationship
    _assetcollection_oid = Column(
        BigInteger,
        ForeignKey('loss_assetcollection._oid', ondelete="CASCADE"))
    assetcollection = relationship(
        'AssetCollection',
        back_populates='sites')

    assets = relationship(
        'Asset',
        back_populates='site')
