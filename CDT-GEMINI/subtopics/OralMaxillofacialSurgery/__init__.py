"""
Module for handling dental oral and maxillofacial surgery code extraction.
"""

from .extractions import activate_extractions
from .other_surgical_procedures import activate_other_surgical_procedures
from .alveoloplasty import activate_alveoloplasty
from .vestibuloplasty import activate_vestibuloplasty
from .excision_soft_tissue import activate_excision_soft_tissue
from .excision_intra_osseous import activate_excision_intra_osseous
from .excision_bone_tissue import activate_excision_bone_tissue
from .surgical_incision import activate_surgical_incision
from .closed_fractures import activate_closed_fractures
from .open_fractures import activate_open_fractures
from .tmj_dysfunctions import activate_tmj_dysfunctions
from .traumatic_wounds import activate_traumatic_wounds
from .complicated_suturing import activate_complicated_suturing
from .other_repair_procedures import activate_other_repair_procedures

__all__ = [
    'activate_extractions',
    'activate_other_surgical_procedures',
    'activate_alveoloplasty',
    'activate_vestibuloplasty',
    'activate_excision_soft_tissue',
    'activate_excision_intra_osseous',
    'activate_excision_bone_tissue',
    'activate_surgical_incision',
    'activate_closed_fractures',
    'activate_open_fractures',
    'activate_tmj_dysfunctions',
    'activate_traumatic_wounds',
    'activate_complicated_suturing',
    'activate_other_repair_procedures'
] 