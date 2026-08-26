from .ztf import ZTFDataSource
from .gaia import GaiaDataSource

DATA_SOURCES = {
    "gaia": GaiaDataSource(),
    "ztf": ZTFDataSource()
}