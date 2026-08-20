from dataclasses import dataclass

@dataclass
class SourceID:
    catalogue: str # ZTF, Gaia etc
    id: str

@dataclass
class GaiaData:
    parallax: float | None
    parallax_error: float | None
    parallax_over_error: float | None

    phot_bp_mean_mag: float | None
    phot_rp_mean_mag: float | None
    phot_g_mean_mag: float | None
    bp_rp: float | None
# TODO: Add number of observations to GaiaData

@dataclass
class ZTFData:
    filtercode: str | None
    nobs: int | None
    ngoodobs: float | None
    weightedmeanmag: float | None
    weightedmagrms: float | None
    chisq: float | None

@dataclass
class Star:
    id: str
    ra: float
    dec: float
    source_ids:  list[SourceID]
    gaia_data: GaiaData | None
    ztf_data: ZTFData | None


