"""
Module to handle dental code extraction.
This module imports and exposes activation functions for dental code extraction.
"""

from .diagnostics import activate_diagnostic, analyze_diagnostic
from .endodontics import activate_endodontic, analyze_endodontic
from .implantservices import activate_implant_services, analyze_implant_services
from .maxillofacialprosthetics import activate_maxillofacial_prosthetics, analyze_maxillofacial_prosthetics
from .oralandmaxillofacialsurgery import activate_oral_maxillofacial_surgery, analyze_oral_maxillofacial_surgery
from .orthodontics import activate_orthodontic, analyze_orthodontic
from .periodontics import activate_periodontic, analyze_periodontic
from .preventive import activate_preventive, analyze_preventive
from .prosthodonticsfixed import activate_prosthodonticsfixed, analyze_prosthodonticsfixed
from .prosthodonticsremovable import activate_prosthodonticsremovable, analyze_prosthodonticsremovable
from .restorative import activate_restorative, analyze_restorative
from .adjunctivegeneralservices import activate_adjunctive_general_services, analyze_adjunctive_general_services

__all__ = [
    'activate_diagnostic',
    'analyze_diagnostic',
    'activate_endodontic',
    'analyze_endodontic',
    'activate_implant_services',
    'analyze_implant_services',
    'activate_maxillofacial_prosthetics',
    'analyze_maxillofacial_prosthetics',
    'activate_oral_maxillofacial_surgery',
    'analyze_oral_maxillofacial_surgery',
    'activate_orthodontic',
    'analyze_orthodontic',
    'activate_periodontic',
    'analyze_periodontic',
    'activate_preventive',
    'analyze_preventive',
    'activate_prosthodonticsfixed',
    'analyze_prosthodonticsfixed',
    'activate_prosthodonticsremovable',
    'analyze_prosthodonticsremovable',
    'activate_restorative',
    'analyze_restorative',
    'activate_adjunctive_general_services',
    'analyze_adjunctive_general_services'
]