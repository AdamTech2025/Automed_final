from .clinicaloralevaluation import activate_clinical_oral_evaluations
from .diagnosticimaging import activate_diagnostic_imaging
from .oralpathologylaboratory import activate_oral_pathology_laboratory
from .prediagnosticservices import activate_prediagnostic_services as activate_pre_diagnostic_services
from .testsandexaminations import activate_tests_and_examinations as activate_tests_and_laboratory_examinations

__all__ = [
    "activate_clinical_oral_evaluations", 
    "activate_diagnostic_imaging", 
    "activate_oral_pathology_laboratory", 
    "activate_pre_diagnostic_services", 
    "activate_tests_and_laboratory_examinations"
]