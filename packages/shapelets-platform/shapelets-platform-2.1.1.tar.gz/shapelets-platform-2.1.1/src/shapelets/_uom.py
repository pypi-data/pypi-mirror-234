from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

import numpy as np

from shapelets_native import (
    convert_unit as _convert_unit, parse_unit as _parse_unit,
    Unit, UnitPriority, UnitStandard, AngleUnits, AreaUnits,
    AustraliaUnits, AvoirdupoisUnits, BritishUnits, CGSUnits,
    CanadaUnits, ChinaUnits, ClimateUnits, ClinicalUnits,
    ComputationUnits, DataUnits, DistanceUnits, ElectricalUnits,
    EnergyUnits, FDAUnits, GFUnits, InternationalUnits, JapanUnits,
    LaboratoryUnits, LogUnits, MTSUnits, MassUnits, NauticalUnits,
    OtherUnits, PharmaUnits, PowerUnits, Prefixes, PressureUnits,
    SpecialUnits, TemperatureUnits, TimeCatalogue, TextileUnits,
    TroyUnits, USAUnits, USADryUnits, USAEngUnits, USAGrainUnits,
    SIUnits, VolumeUnits, UnitsCatalogue
)

UnitLike = Union[str, Unit]


@dataclass
class ParseUnitDefaults:
    case_insensitive: bool = False
    priority: UnitPriority = UnitPriority.NoPriority
    standard: UnitStandard = UnitStandard.NoStandard


_parse_defaults: ParseUnitDefaults = ParseUnitDefaults()


def parse_unit_defaults(caseInsensitive: Optional[bool] = None, priority: Optional[UnitPriority] = None, standard: Optional[UnitStandard] = None) -> ParseUnitDefaults:
    global _parse_defaults
    _parse_defaults = ParseUnitDefaults(
        caseInsensitive if caseInsensitive is not None else _parse_defaults.case_insensitive,
        priority if priority is not None else _parse_defaults.priority,
        standard if standard is not None else _parse_defaults.standard)

    return _parse_defaults


def parse_unit(expr: UnitLike, caseInsensitive: Optional[bool] = None, priority: Optional[UnitPriority] = None, standard: Optional[UnitStandard] = None) -> Unit:

    # if it is already a unit, just return it
    if isinstance(expr, Unit):
        return expr

    # otherwise, try to parse, using the parameters or
    # the default values
    result = _parse_unit(expr,
                         caseInsensitive if caseInsensitive is not None else _parse_defaults.case_insensitive,
                         priority if priority is not None else _parse_defaults.priority,
                         standard if standard is not None else _parse_defaults.standard)
    if result is None:
        raise ValueError(f'[{expr}] did not yield a valid Unit')

    return result


def convert_unit(src: UnitLike, dst: UnitLike, values: np.ndarray[np.float64]) -> Union[np.float64, np.ndarray[np.float64]]:
    r"""
    Converts magnitudes expressed in one unit to another unit

    Parameters
    ----------
    src: a string or an Unit object
        Source units
    dst: a string or an Unit object
        Destination units
    values: NumPy array like
        Values to be converted

    Returns
    -------
    Either a float or a NumPy array of floats
        The result will vary to match the cardinality of the values parameter

    Notes
    -----
    This is NumPy vectorized function

    Examples
    --------
    >>> import shapelets as sh
    >>> sh.convert_unit("km/h", "m/s", [1.0, 2.0, 3.0])
    array([0.27777778, 0.55555556, 0.83333333])
    >>> sh.convert_unit("km/h", "m/s", 1.0)
    0.2777777777777778
    """
    return _convert_unit(parse_unit(src), parse_unit(dst), values)


units = UnitsCatalogue()
r"""
Catalogue of pre-built units
"""

__all__ = [
    'units', 'Unit', 'UnitLike', 'convert_unit', 'UnitPriority', 'UnitStandard', 'parse_unit', 'parse_unit_defaults',
    'AngleUnits', 'AreaUnits', 'AustraliaUnits', 'AvoirdupoisUnits', 'BritishUnits', 'CGSUnits',
    'CanadaUnits', 'ChinaUnits', 'ClimateUnits', 'ClinicalUnits', 'ComputationUnits',
    'DataUnits', 'DistanceUnits', 'ElectricalUnits', 'EnergyUnits', 'FDAUnits', 'GFUnits',
    'InternationalUnits', 'JapanUnits', 'LaboratoryUnits', 'LogUnits', 'MTSUnits', 'MassUnits',
    'NauticalUnits', 'OtherUnits', 'PharmaUnits', 'PowerUnits', 'Prefixes', 'PressureUnits',
    'SpecialUnits', 'TemperatureUnits', 'TextileUnits', 'TimeCatalogue', 'TroyUnits', 'USAUnits', 'USADryUnits',
    'USAEngUnits', 'USAGrainUnits', 'SIUnits', 'VolumeUnits', 'UnitsCatalogue'
]
