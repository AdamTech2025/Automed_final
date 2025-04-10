"""
Module to handle restorative dental code extraction.
This module imports and exposes activation functions for different restorative service subtopics.
"""

from subtopics.Restorative.amalgam_restorations import activate_amalgam_restorations
from subtopics.Restorative.resin_based_composite_restorations import activate_resin_based_composite_restorations
from subtopics.Restorative.gold_foil_restorations import activate_gold_foil_restorations
from subtopics.Restorative.inlays_and_onlays import activate_inlays_and_onlays
from subtopics.Restorative.crowns import activate_crowns
from subtopics.Restorative.other_restorative_services import activate_other_restorative_services

__all__ = [
    'activate_amalgam_restorations',
    'activate_resin_based_composite_restorations',
    'activate_gold_foil_restorations',
    'activate_inlays_and_onlays',
    'activate_crowns',
    'activate_other_restorative_services',
] 