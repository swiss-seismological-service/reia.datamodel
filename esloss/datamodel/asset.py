from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import (
    BigInteger, Integer, String, Boolean, Float)

from esloss.datamodel.base import ORMBase
from esloss.datamodel.mixins import (
    ClassificationMixin, CreationInfoMixin, PublicIdMixin)


class AssetCollection(ORMBase, PublicIdMixin, CreationInfoMixin):
    """Asset Collection model"""
    name = Column(String)
    category = Column(String)
    description = Column(String)
    taxonomysource = Column(String)
    dayoccupancy = Column(Boolean,
                          server_default='false',
                          default=False,
                          nullable=False)
    nightoccupancy = Column(Boolean,
                            server_default='false',
                            default=False,
                            nullable=False)
    transitoccupancy = Column(Boolean,
                              server_default='false',
                              default=False,
                              nullable=False)

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

    aggregationtags = relationship('AggregationTag',
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


class Asset(PublicIdMixin, ClassificationMixin('taxonomy'), ORMBase):
    """Asset model"""

    buildingcount = Column(Integer, nullable=False)

    contentsvalue = Column(Float)
    structuralvalue = Column(Float)
    nonstructuralvalue = Column(Float)
    dayoccupancy = Column(Float)
    nightoccupancy = Column(Float)
    transitoccupancy = Column(Float)
    businessinterruptionvalue = Column(Float)

    _aggregationtag_oid = Column(
        BigInteger, ForeignKey('loss_aggregationtag._oid'))
    aggregationtag = relationship(
        'AggregationTag',
        backref='assets')

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


class Site(PublicIdMixin, ORMBase):
    """Site model"""

    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

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


class AggregationTag(ORMBase):
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    # asset collection relationship
    _assetcollection_oid = Column(
        BigInteger,
        ForeignKey('loss_assetcollection._oid', ondelete="CASCADE"))
    assetcollection = relationship(
        'AssetCollection',
        back_populates='aggregationtag')
