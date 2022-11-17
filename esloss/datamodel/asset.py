from sqlalchemy import Table, delete, event
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Float, Integer, String

from esloss.datamodel.base import ORMBase
from esloss.datamodel.lossvalues import riskvalue_aggregationtag
from esloss.datamodel.mixins import (ClassificationMixin, CreationInfoMixin,
                                     PublicIdMixin)


class ExposureModel(ORMBase,
                    PublicIdMixin,
                    CreationInfoMixin,
                    ClassificationMixin('taxonomy')):
    '''Asset Collection model'''
    name = Column(String)
    category = Column(String)
    description = Column(String)
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

    costtypes = relationship('CostType', back_populates='exposuremodel',
                             passive_deletes=True,
                             cascade='all, delete-orphan',
                             lazy='joined')

    calculationbranch = relationship('CalculationBranch',
                                     back_populates='exposuremodel')

    assets = relationship('Asset',
                          back_populates='exposuremodel',
                          passive_deletes=True,
                          cascade='all, delete-orphan')
    sites = relationship('Site',
                         back_populates='exposuremodel',
                         passive_deletes=True,
                         cascade='all, delete-orphan')


class CostType(ORMBase):
    name = Column(String)
    type = Column(String)
    unit = Column(String)

    _exposuremodel_oid = Column(BigInteger, ForeignKey(
        'loss_exposuremodel._oid', ondelete='CASCADE'))
    exposuremodel = relationship(
        'ExposureModel',
        back_populates='costtypes')


asset_aggregationtag = Table(
    'loss_assoc_asset_aggregationtag',
    ORMBase.metadata,
    Column('asset',
           ForeignKey('loss_asset._oid',
                      ondelete='CASCADE'),
           primary_key=True),
    Column('aggregationtag',
           ForeignKey('loss_aggregationtag._oid',
                      ondelete='CASCADE'),
           primary_key=True),
)


class Asset(ClassificationMixin('taxonomy'), ORMBase):
    '''Asset model'''

    buildingcount = Column(Integer, nullable=False)

    contentsvalue = Column(Float)
    structuralvalue = Column(Float)
    nonstructuralvalue = Column(Float)
    dayoccupancy = Column(Float)
    nightoccupancy = Column(Float)
    transitoccupancy = Column(Float)
    businessinterruptionvalue = Column(Float)

    aggregationtags = relationship('AggregationTag',
                                   secondary=asset_aggregationtag,
                                   back_populates='assets',
                                   lazy='joined')

    _exposuremodel_oid = Column(BigInteger,
                                ForeignKey('loss_exposuremodel._oid',
                                           ondelete='CASCADE'))
    exposuremodel = relationship('ExposureModel',
                                 back_populates='assets')

    # site relationship
    _site_oid = Column(BigInteger,
                       ForeignKey('loss_site._oid'),
                       nullable=False)
    site = relationship('Site',
                        back_populates='assets',
                        lazy='joined')


class Site(ORMBase):
    '''Site model'''

    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

    # asset collection relationship
    _exposuremodel_oid = Column(
        BigInteger,
        ForeignKey('loss_exposuremodel._oid', ondelete='CASCADE'))
    exposuremodel = relationship(
        'ExposureModel',
        back_populates='sites')

    assets = relationship(
        'Asset',
        back_populates='site')


class AggregationTag(ORMBase):
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    assets = relationship(
        'Asset', secondary=asset_aggregationtag,
        back_populates='aggregationtags')

    riskvalues = relationship(
        'RiskValue', secondary=riskvalue_aggregationtag,
        back_populates='aggregationtags'
    )

# Make sure that Aggregationtags which don't have a parent anymore
# (meaning neither referenced by a LossValue nor an Asset) are deleted


@event.listens_for(Session, 'do_orm_execute', once=True)
def delete_tag_orphans_execute(orm_execute_state):
    if orm_execute_state.is_delete:

        orm_execute_state.invoke_statement()

        stmt = delete(AggregationTag).filter(
            ~AggregationTag.riskvalues.any(),
            ~AggregationTag.assets.any()).execution_options(
            synchronize_session=False)
        orm_execute_state.session.execute(stmt)


@event.listens_for(Session, 'after_flush')
def delete_tag_orphans_session(session, ctx):
    if session.deleted:
        session.query(AggregationTag).\
            filter(
            ~AggregationTag.riskvalues.any(),
            ~AggregationTag.assets.any()).\
            delete(synchronize_session=False)
