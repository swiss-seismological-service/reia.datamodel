from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Integer, String

from esloss.datamodel.mixins import RealQuantityMixin
from esloss.datamodel.base import ORMBase


class LossValue(ORMBase, RealQuantityMixin('loss')):
    """Loss Value"""
    __tablename__ = 'loss_lossvalue'

    _losscalculation_oid = Column(
        BigInteger,
        ForeignKey('loss_losscalculation._oid'),
        nullable=False)
    losscalculation = relationship(
        'LossCalculation',
        back_populates='losses')

    # id of the realization
    eventid = Column(Integer, nullable=False)

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_on': _type,
        'polymorphic_identity': 'loss',
    }


class AggregatedLoss(LossValue):
    """Loss by Aggregation Tag"""

    _aggregationtag_oid = Column(BigInteger,
                                 ForeignKey('loss_aggregationtag._oid'))
    aggregationtag = relationship(
        'AggregationTag',
        back_populates='lossvalues')

    __mapper_args__ = {
        'polymorphic_identity': 'aggregatedloss'
    }


class SiteLoss(LossValue):
    """Loss by site"""

    _site_oid = Column(
        BigInteger,
        ForeignKey('loss_site._oid'),
        nullable=False
    )
    site = relationship('Site')

    __mapper_args__ = {
        'polymorphic_identity': 'siteloss'
    }
