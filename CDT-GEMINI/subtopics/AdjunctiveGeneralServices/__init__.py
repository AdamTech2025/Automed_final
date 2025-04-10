"""
Module to handle adjunctive general services dental code extraction.
This module imports and exposes activation functions for different adjunctive general services subtopics.
"""

from subtopics.AdjunctiveGeneralServices.unclassified_treatment import activate_unclassified_treatment
from subtopics.AdjunctiveGeneralServices.anesthesia import activate_anesthesia
from subtopics.AdjunctiveGeneralServices.professional_consultation import activate_professional_consultation
from subtopics.AdjunctiveGeneralServices.professional_visits import activate_professional_visits
from subtopics.AdjunctiveGeneralServices.drugs import activate_drugs
from subtopics.AdjunctiveGeneralServices.miscellaneous_services import activate_miscellaneous_services
from subtopics.AdjunctiveGeneralServices.non_clinical_procedures import activate_non_clinical_procedures

__all__ = [
    'activate_unclassified_treatment',
    'activate_anesthesia',
    'activate_professional_consultation',
    'activate_professional_visits',
    'activate_drugs',
    'activate_miscellaneous_services',
    'activate_non_clinical_procedures',
] 