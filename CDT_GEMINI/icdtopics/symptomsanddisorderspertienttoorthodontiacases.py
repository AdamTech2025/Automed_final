"""
Module for extracting symptoms and disorders pertinent to orthodontia cases ICD-10 codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Import modules
from icdtopics.prompt import PROMPT

class OrthodontiaCasesServices:
    """Class to analyze and extract symptoms and disorders pertinent to orthodontia cases ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing symptoms and disorders pertinent to orthodontia cases."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in symptoms and disorders pertinent to orthodontia cases. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

18.1 Neurological and Muscular Disorders:
- G24.3: Spasmodic torticollis
- G24.4: Idiopathic orofacial dystonia (Orofacial dyskinesia)

18.2 Headache and Pain Disorders:
- G44.1: Vascular headache, not elsewhere classified
- G44.201: Tension-type headache, unspecified, intractable
- G44.209: Tension-type headache, unspecified, not intractable
- G44.211: Episodic tension-type headache, intractable
- G44.219: Episodic tension-type headache, not intractable
- G44.221: Chronic tension-type headache, intractable
- G44.229: Chronic tension-type headache, not intractable
- H57.11: Ocular pain, right eye
- H57.12: Ocular pain, left eye
- H57.13: Ocular pain, bilateral
- M79.11: Myalgia of mastication muscle
- M79.12: Myalgia of auxiliary muscles, head and neck
- M79.18: Myalgia, other site

18.3 Migraine Disorders:
- G43.001: Migraine without aura, not intractable, with status migrainosus
- G43.009: Migraine without aura, not intractable, without status migrainosus
- G43.011: Migraine without aura, intractable, with status migrainosus
- G43.019: Migraine without aura, intractable, without status migrainosus
- G43.101: Migraine with aura, not intractable, with status migrainosus
- G43.109: Migraine with aura, not intractable, without status migrainosus
- G43.111: Migraine with aura, intractable, with status migrainosus
- G43.119: Migraine with aura, intractable, without status migrainosus
- G43.701: Chronic migraine without aura, not intractable, with status migrainosus
- G43.719: Chronic migraine without aura, not intractable, without status migrainosus
- G43.801: Other migraine, not intractable, with status migrainosus
- G43.809: Other migraine, not intractable, without status migrainosus
- G43.811: Other migraine, intractable, with status migrainosus
- G43.819: Other migraine, intractable, without status migrainosus

18.4 Ears and Larynx Disorders:
- H92.01: Otalgia, right ear
- H92.02: Otalgia, left ear
- H92.03: Otalgia, bilateral
- H93.11: Tinnitus, right ear
- H93.12: Tinnitus, left ear
- H93.13: Tinnitus, bilateral
- J38.5: Laryngeal spasm

18.5 Craniofacial Disorders and Malformations:
- Q67.0: Congenital facial asymmetry
- Q67.4: Other congenital deformities of skull, face, and jaw
- Q74.0: Other congenital malformations of upper limb(s), including shoulder girdle (Includes Cleidocranial dysostosis)
- Q75.0: Craniosynostosis (Pierre Robin Sequence)
- Q75.1: Craniofacial dysostosis (Crouzon's disease [syndrome])
- Q75.2: Hypertelorism
- Q75.3: Macrocephaly
- Q75.4: Mandibulofacial dysostosis (Treacher Collins syndrome)
- Q75.5: Oculomandibular dysostosis
- Q75.8: Other specified malformations of skull and face bones
- Q75.9: Congenital malformation of skull and face bones, unspecified
- Q87.0: Congenital malformation syndromes predominantly affecting facial appearance (Includes Acrocephalopolysyndactyly [Apert Syndrome and Pfeiffer Syndrome])
- Q87.19: Other congenital malformation syndromes predominantly associated with short stature (Includes Noonan syndrome)

18.6 Turner's Syndrome:
- Q96.0: Karyotype 45, X
- Q96.2: Karyotype 46, X with abnormal sex chromosome, except iso (Xq)
- Q96.3: Mosaicism, 45, X/46, XX or XY
- Q96.4: Mosaicism, 45, X/other cell line(s) with abnormal sex chromosome
- Q96.8: Other variants of Turner's Syndrome
- Q96.9: Turner's Syndrome, unspecified

18.7 Endocrine and Growth Disorders:
- E22.0: Acromegaly and pituitary gigantism
- E23.0: Hypopituitarism (Includes isolated deficiency of growth hormone)

18.8 Other Disorders:
- G25.3: Myoclonus
- R42: Dizziness and giddiness (Includes light-headedness)
- K00.9: Disorder of tooth development and eruption, unspecified (Disorder of odontogenesis NOS)

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_orthodontia_cases_code(self, scenario: str) -> str:
        """Extract symptoms and disorders pertinent to orthodontia cases code(s) for a given scenario."""
        try:
            print(f"Analyzing orthodontia cases scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Orthodontia cases extract_orthodontia_cases_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in orthodontia cases code extraction: {str(e)}")
            return ""
    
    def activate_orthodontia_cases(self, scenario: str) -> str:
        """Activate the orthodontia cases analysis process and return results."""
        try:
            result = self.extract_orthodontia_cases_code(scenario)
            if not result:
                print("No orthodontia cases code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating orthodontia cases analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_orthodontia_cases(scenario)
        print(f"\n=== ORTHODONTIA CASES ANALYSIS RESULT ===")
        print(f"ORTHODONTIA CASES CODE: {result if result else 'None'}")


orthodontia_cases_service = OrthodontiaCasesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an orthodontia cases dental scenario: ")
    orthodontia_cases_service.run_analysis(scenario)
