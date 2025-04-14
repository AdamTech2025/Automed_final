"""
Module for extracting findings of bost teeth ICD-10 codes.
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
 
def create_bost_teeth_findings_extractor(temperature=0.0):
    """
    Create a LangChain-based bost teeth findings code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in findings of bost teeth. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

10.1 Findings of Bost Teeth:
- K08.121: Complete loss of teeth due to trauma, class I
- K08.122: Complete loss of teeth due to trauma, class II
- K08.123: Complete loss of teeth due to trauma, class III
- K08.124: Complete loss of teeth due to trauma, class IV
- K08.129: Complete loss of teeth due to trauma, unspecified class
- K08.131: Complete loss of teeth due to periodontal diseases, class I
- K08.132: Complete loss of teeth due to periodontal diseases, class II
- K08.133: Complete loss of teeth due to periodontal diseases, class III
- K08.134: Complete loss of teeth due to periodontal diseases, class IV
- K08.139: Complete loss of teeth due to periodontal diseases, unspecified class
- K08.191: Complete loss of teeth due to other specified cause, class I
- K08.192: Complete loss of teeth due to other specified cause, class II
- K08.193: Complete loss of teeth due to other specified cause, class III
- K08.194: Complete loss of teeth due to other specified cause, class IV
- K08.199: Complete loss of teeth due to other specified cause, unspecified class

Scenario: {scenario}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_bost_teeth_findings_code(scenario, temperature=0.0):
    """
    Extract bost teeth findings code(s) for a given scenario.
    """
    try:
        chain = create_bost_teeth_findings_extractor(temperature)
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
            
        print(f"Bost teeth findings code result: {result_text}")
        return result_text.strip()
    except Exception as e:
        print(f"Error in extract_bost_teeth_findings_code: {str(e)}")
        return ""

def activate_lost_teeth(scenario):
    """
    Activate bost teeth findings analysis and return results.
    """
    try:
        return extract_bost_teeth_findings_code(scenario)
    except Exception as e:
        print(f"Error in activate_lost_teeth: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient has complete loss of teeth due to periodontal disease, class II configuration."
    result = activate_lost_teeth(scenario)
    print(result) 