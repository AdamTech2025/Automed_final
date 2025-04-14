"""
Module for extracting diseases and conditions of the periodontium ICD-10 codes.
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
 
def create_periodontium_diseases_extractor(temperature=0.0):
    """
    Create a LangChain-based periodontium diseases code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in diseases and conditions of the periodontium. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Diseases and Conditions of the Periodontium ICD-10 codes include:
5.1 Gingivitis
- K05.00: Acute gingivitis, plaque induced
- K05.01: Acute gingivitis, non-plaque induced
- K05.10: Chronic gingivitis, plaque induced
- K05.11: Chronic gingivitis, non-plaque induced

5.2 Gingival Recession
- K06.011: Localized gingival recession, minimal
- K06.012: Localized gingival recession, moderate
- K06.013: Localized gingival recession, severe
- K06.021: Generalized gingival recession, minimal
- K06.022: Generalized gingival recession, moderate
- K06.023: Generalized gingival recession, severe

5.3 Other Gingival Conditions
- K06.1: Gingival enlargement
- K06.2: Gingival and edentulous alveolar ridge lesions associated with trauma
- K06.3: Horizontal alveolar bone loss
- K06.8: Other specified disorders of gingiva and edentulous alveolar ridge

5.4 Periodontitis
- K05.211: Aggressive periodontitis, localized, slight
- K05.212: Aggressive periodontitis, localized, moderate
- K05.213: Aggressive periodontitis, localized, severe
- K05.219: Aggressive periodontitis, localized, unspecified severity
- K05.221: Aggressive periodontitis, generalized, slight
- K05.222: Aggressive periodontitis, generalized, moderate
- K05.223: Aggressive periodontitis, generalized, severe
- K05.311: Chronic periodontitis, localized, slight
- K05.312: Chronic periodontitis, localized, moderate
- K05.313: Chronic periodontitis, localized, severe
- K05.321: Chronic periodontitis, generalized, slight
- K05.322: Chronic periodontitis, generalized, moderate
- K05.323: Chronic periodontitis, generalized, severe
- K05.4: Periodontosis
- K05.5: Other periodontal disease

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_periodontium_diseases_code(scenario, temperature=0.0):
    """
    Extract periodontium diseases code(s) for a given scenario.
    """
    try:
        chain = create_periodontium_diseases_extractor(temperature)
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
        print(f"Error in extract_periodontium_diseases_code: {str(e)}")
        return ""

def activate_periodontium_disorders(scenario):
    """
    Activate periodontium diseases analysis and return results.
    """
    try:
        return extract_periodontium_diseases_code(scenario)
    except Exception as e:
        print(f"Error in activate_periodontium_disorders: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with severe localized gingival recession on multiple teeth."
    result = activate_periodontium_disorders(scenario)
    print(result)
