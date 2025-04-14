"""
Module for extracting disorders of teeth ICD-10 codes.
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
 
def create_teeth_disorders_extractor(temperature=0.0):
    """
    Create a LangChain-based teeth disorders code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in disorders of teeth. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Disorders of Teeth ICD-10 codes include:
3.1 Occlusal Trauma
- K08.81: Primary occlusal trauma
- K08.82: Secondary occlusal trauma
- K08.89: Other specified disorders of teeth and supporting structures
  (Includes: Enlargement of alveolar ridge NOS, Insufficient anatomic crown height, 
   Insufficient clinical crown length, Irregular alveolar process, Toothache NOS)

3.2 Tooth Wear
- K03.0: Excessive attrition of teeth
- K03.1: Abrasion of teeth
- K03.2: Erosion of teeth
- K03.3: Pathological resorption of teeth

3.3 Other Disorders
- K03.4: Hypercementosis
- K03.5: Ankylosis of teeth
- K03.6: Deposits [accretions] on teeth
- K03.7: Posteruptive color changes of dental hard tissues
- K03.81: Cracked tooth
- K03.89: Other specified diseases of hard tissues of teeth
- K03.9: Disease of hard tissues of teeth, unspecified

9.2 Tooth Loss:
- K08.109: Complete loss of teeth, unspecified cause, unspecified class
- K08.419: Partial loss of teeth, unspecified cause, unspecified class
- K08.3: Retained dental root
- K08.401: Partial loss of teeth, unspecified cause, class I
- K08.402: Partial loss of teeth, unspecified cause, class II
- K08.403: Partial loss of teeth, unspecified cause, class III
- K08.404: Partial loss of teeth, unspecified cause, class IV

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_teeth_disorders_code(scenario, temperature=0.0):
    """
    Extract teeth disorders code(s) for a given scenario.
    """
    try:
        chain = create_teeth_disorders_extractor(temperature)
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
        print(f"Error in extract_teeth_disorders_code: {str(e)}")
        return ""

def activate_disorders_of_teeth(scenario):
    """
    Activate teeth disorders analysis and return results.
    """
    try:
        return extract_teeth_disorders_code(scenario)
    except Exception as e:
        print(f"Error in activate_disorders_of_teeth: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with severe tooth wear due to grinding."
    result = activate_disorders_of_teeth(scenario)
    print(result)
