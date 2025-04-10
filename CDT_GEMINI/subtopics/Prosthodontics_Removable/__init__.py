"""
Module to handle dental removable prosthodontics code extraction.
This module imports and exposes activation functions related to removable prosthodontics.
"""

from .complete_dentures import activate_complete_dentures
from .partial_denture import activate_partial_denture
from .adjustments_to_dentures import activate_adjustments_to_dentures
from .repairs_to_complete_dentures import activate_repairs_to_complete_dentures
from .repairs_to_partial_dentures import activate_repairs_to_partial_dentures
from .denture_rebase_procedures import activate_denture_rebase_procedures
from .denture_reline_procedures import activate_denture_reline_procedures
from .interim_prosthesis import activate_interim_prosthesis
from .other_removable_prosthetic_services import activate_other_removable_prosthetic_services

__all__ = [
    'activate_complete_dentures',
    'activate_partial_denture',
    'activate_adjustments_to_dentures',
    'activate_repairs_to_complete_dentures',
    'activate_repairs_to_partial_dentures',
    'activate_denture_rebase_procedures',
    'activate_denture_reline_procedures',
    'activate_interim_prosthesis',
    'activate_other_removable_prosthetic_services'
] 