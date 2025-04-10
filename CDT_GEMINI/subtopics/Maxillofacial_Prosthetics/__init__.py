"""
Module for handling dental maxillofacial prosthetics code extraction.
"""

from .general_prosthetics import activate_general_prosthetics
from .carriers import activate_carriers

__all__ = [
    'activate_general_prosthetics',
    'activate_carriers'
] 