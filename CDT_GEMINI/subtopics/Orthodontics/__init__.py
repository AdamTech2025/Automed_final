"""
Module for handling dental orthodontic code extraction.
"""

from .limited_orthodontic_treatment import activate_limited_orthodontic_treatment
from .comprehensive_orthodontic_treatment import activate_comprehensive_orthodontic_treatment
from .minor_treatment_harmful_habits import activate_minor_treatment_harmful_habits
from .other_orthodontic_services import activate_other_orthodontic_services

__all__ = [
    'activate_limited_orthodontic_treatment',
    'activate_comprehensive_orthodontic_treatment',
    'activate_minor_treatment_harmful_habits',
    'activate_other_orthodontic_services'
] 