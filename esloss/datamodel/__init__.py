
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from esloss.datamodel.asset import (
    AssetCollection, Asset, Site, Municipality, PostalCode, Canton)
from esloss.datamodel.lossmodel import (LossModel, LossCalculation, LossConfig)
from esloss.datamodel.vulnerability import (
    VulnerabilityFunction, VulnerabilityModel)
from esloss.datamodel.lossvalues import (
    MeanAssetLoss, SiteLoss, TaxonomyLoss, MunicipalityPCLoss)

class Base(object):

    @ declared_attr
    def __tablename__(cls):
        return f'loss_{cls.__name__.lower()}'

    _oid = Column(BigInteger, primary_key=True)

    def _asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_


ORMBase = declarative_base(cls=Base)