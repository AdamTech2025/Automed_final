"""
Module for handling dental maxillofacial prosthetics code extraction.
"""

from .general_prosthetics import activate_general_prosthetics, create_general_prosthetics_extractor, extract_general_prosthetics_code
from .carriers import activate_carriers, create_carriers_extractor, extract_carriers_code

__all__ = [
    'activate_general_prosthetics',
    'create_general_prosthetics_extractor',
    'extract_general_prosthetics_code',
    'activate_carriers',
    'create_carriers_extractor',
    'extract_carriers_code'
] 