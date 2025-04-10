"""
Module for handling dental periodontal code extraction.
"""

from .surgical_services import activate_surgical_services
from .non_surgical_services import activate_non_surgical_services
from .other_periodontal_services import activate_other_periodontal_services

__all__ = [
    'activate_surgical_services',
    'activate_non_surgical_services',
    'activate_other_periodontal_services'
] 