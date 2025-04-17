"""
Module for extracting pathologies ICD-10 codes.
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

class PathologiesServices:
    """Class to analyze and extract pathologies ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing pathologies."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in pathologies. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

15.1 Jaw-Related Disorders:
- M27.0: Developmental disorders of jaws
- M27.1: Giant cell granuloma, central
- M27.2: Inflammatory conditions of jaws
- M27.3: Alveolitis of jaws
- M27.40: Unspecified cyst of jaw
- M27.49: Other cysts of jaw
- M27.8: Other specified diseases of jaws

15.2 Cysts of the Oral Region:
- K09.0: Developmental odontogenic cysts
- K09.1: Developmental (nonodontogenic) cysts of oral region
- K09.8: Other cysts of oral region, not elsewhere classified

15.3 Disorders of Salivary Glands:
- K11.0: Atrophy of salivary gland
- K11.1: Hypertrophy of salivary gland
- K11.21: Acute sialoadenitis
- K11.22: Acute recurrent sialoadenitis
- K11.23: Chronic sialoadenitis
- K11.3: Abscess of salivary gland
- K11.4: Fistula of salivary gland
- K11.5: Sialolithiasis (salivary stones)
- K11.6: Mucocele of salivary gland
- K11.7: Disturbances of salivary secretion
- K11.8: Other diseases of salivary glands

15.4 Diseases of Lips and Oral Mucosa:
- K13.1: Cheek and lip biting
- K13.21: Leukoplakia of oral mucosa, including tongue
- K13.22: Minimal keratinized residual ridge mucosa
- K13.23: Excessive keratinized residual ridge mucosa
- K13.24: Leukokeratosis nicotina palate (nicotine-induced leukoplakia)
- K13.29: Other disturbances of oral epithelium, including tongue
- K13.3: Hairy leukoplakia
- K13.4: Granuloma and granuloma-like lesions of oral mucosa
- K13.5: Oral submucous fibrosis
- K13.6: Irritative hyperplasia of oral mucosa
- K13.79: Other lesions of oral mucosa

15.5 Disorders of the Tongue:
- K14.0: Glossitis (inflammation of the tongue)
- K14.1: Geographic tongue (benign migratory glossitis)
- K14.2: Median rhomboid glossitis
- K14.3: Hypertrophy of tongue papillae
- K14.4: Atrophy of tongue papillae
- K14.5: Plicated tongue (fissured tongue)
- K14.6: Glossodynia (burning tongue syndrome)
- K14.8: Other diseases of the tongue

15.6 Disorders of Skin and Subcutaneous Tissues:
- L40.52: Psoriatic arthritis mutilans
- L40.54: Psoriatic juvenile arthropathy
- L40.59: Other psoriatic arthropathy
- L43.9: Lichen planus, unspecified
- L90.5: Scar conditions and fibrosis of skin

15.7 Musculoskeletal System and Connective Tissue Disorders:
- M06.9: Rheumatoid arthritis, unspecified
- M08.00: Unspecified juvenile rheumatoid arthritis of unspecified site
- M24.20: Disorder of ligament, unspecified site
- M32.10: Systemic lupus erythematosus, organ or system involvement unspecified
- M35.00: Sjögren syndrome [Sicca], unspecified
- M35.0C: Sjögren syndrome with dental involvement
- M35.7: Hypermobility syndrome
- M43.6: Torticollis (wry neck)
- M45.9: Ankylosing spondylitis of unspecified sites in spine
- M54.2: Cervicalgia (neck pain)
- M60.9: Myositis, unspecified
- M62.40: Contracture of muscle, unspecified site
- M62.81: Muscle weakness (generalized)
- M62.838: Other muscle spasm
- M65.9: Synovitis and tenosynovitis, unspecified
- M79.2: Neuralgia and neuritis, unspecified
- M87.00: Idiopathic aseptic necrosis of unspecified bone
- M87.180: Osteonecrosis due to drugs, jaw

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_pathologies_code(self, scenario: str) -> str:
        """Extract pathologies code(s) for a given scenario."""
        try:
            print(f"Analyzing pathologies scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Pathologies extract_pathologies_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in pathologies code extraction: {str(e)}")
            return ""
    
    def activate_pathologies(self, scenario: str) -> str:
        """Activate the pathologies analysis process and return results."""
        try:
            result = self.extract_pathologies_code(scenario)
            if not result:
                print("No pathologies code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating pathologies analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_pathologies(scenario)
        print(f"\n=== PATHOLOGIES ANALYSIS RESULT ===")
        print(f"PATHOLOGIES CODE: {result if result else 'None'}")


pathologies_service = PathologiesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a pathologies dental scenario: ")
    pathologies_service.run_analysis(scenario)
