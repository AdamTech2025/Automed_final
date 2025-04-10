"""
Module for handling dental fixed prosthodontics code extraction.
"""

from .fixed_partial_denture_pontics import activate_fixed_partial_denture_pontics
from .fixed_partial_denture_retainers_inlays_onlays import activate_fixed_partial_denture_retainers_inlays_onlays
from .fixed_partial_denture_retainers_crowns import activate_fixed_partial_denture_retainers_crowns
from .other_fixed_partial_denture_services import activate_other_fixed_partial_denture_services

__all__ = [
    'activate_fixed_partial_denture_pontics',
    'activate_fixed_partial_denture_retainers_inlays_onlays',
    'activate_fixed_partial_denture_retainers_crowns',
    'activate_other_fixed_partial_denture_services'
] 