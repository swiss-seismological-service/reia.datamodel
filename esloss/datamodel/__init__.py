
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger
from sqlalchemy.ext.declarative import declared_attr

from datamodel.asset import (
    AssetCollection, Asset, Site, Municipality, PostalCode, Canton)
from datamodel.lossmodel import (LossModel, LossCalculation, LossConfig)
from datamodel.vulnerability import (
    VulnerabilityFunction, VulnerabilityModel)
from datamodel.lossvalues import (
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


