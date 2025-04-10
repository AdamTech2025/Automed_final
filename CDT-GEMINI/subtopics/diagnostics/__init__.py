from .clinicaloralevaluation import activate_clinical_oral_evaluations
from .diagnosticimaging import activate_diagnostic_imaging
from .oralpathologylaboratory import activate_oral_pathology_laboratory
from .prediagnosticservices import activate_prediagnostic_services as activate_pre_diagnostic_services
from .testsandexaminations import activate_tests_and_examinations as activate_tests_and_laboratory_examinations

# # Define a placeholder function for the missing assessment function
# def activate_assessment_of_patient_outcome_metrics(scenario):
#     return "D4186 - Assessment of patient outcome metrics"

__all__ = [
    "activate_clinical_oral_evaluations", 
    "activate_diagnostic_imaging", 
    "activate_oral_pathology_laboratory", 
    "activate_pre_diagnostic_services", 
    "activate_tests_and_laboratory_examinations",
    "activate_assessment_of_patient_outcome_metrics"
]