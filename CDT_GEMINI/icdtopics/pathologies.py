"""
Module for extracting pathologies ICD-10 codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from icdtopics.prompt import PROMPT

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_pathologies_extractor(temperature=0.0):
    """
    Create a LangChain-based pathologies code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
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

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_pathologies_code(scenario, temperature=0.0):
    """
    Extract pathologies code(s) for a given scenario.
    """
    try:
        chain = create_pathologies_extractor(temperature)
        result = chain.invoke({"scenario": scenario})
        # Handle different return formats from LangChain
        if isinstance(result, dict):
            if "text" in result:
                result_text = result["text"]
            elif "output_text" in result:
                result_text = result["output_text"]
            else:
                result_text = str(result)
        elif hasattr(result, "content"):
            result_text = result.content
        else:
            result_text = str(result)
        
        print(f"Result: {result_text}")
        return result_text.strip()
    except Exception as e:
        print(f"Error in extract_pathologies_code: {str(e)}")
        return ""

def activate_pathologies(scenario):
    """
    Activate pathologies analysis and return results.
    """
    try:
        return extract_pathologies_code(scenario)
    except Exception as e:
        print(f"Error in activate_pathologies: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with a salivary stone in the submandibular gland."
    result = activate_pathologies(scenario)
    print(result)
