# from stix2.v21.sdo import ATTACK_MOTIVATION, ATTACK_RESOURCE_LEVEL, GROUPING_CONTEXT, INDUSTRY_SECTOR
# from stx2.v21 import EXT_MAP

from stix2.v21 import OBJ_MAP as _OBJ_MAP, OBJ_MAP_OBSERVABLE as _OBJ_MAP_OBSERVABLE
from stix2.v21.common import TLP_AMBER, TLP_GREEN, TLP_RED, TLP_WHITE


SROS = dict(
    relationship=_OBJ_MAP.pop("relationship"),
    sighting=_OBJ_MAP.pop("sighting"),
)
SDOS = _OBJ_MAP
SCOS = _OBJ_MAP_OBSERVABLE

TLP_MARKING = dict(
    white=TLP_WHITE,
    green=TLP_GREEN,
    amber=TLP_AMBER,
    red=TLP_RED,
)
