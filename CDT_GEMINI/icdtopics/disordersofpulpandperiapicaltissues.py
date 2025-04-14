"""
Module for extracting disorders of pulp and periapical tissues ICD-10 codes.
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
 
def create_pulp_periapical_disorders_extractor(temperature=0.0):
    """
    Create a LangChain-based pulp and periapical disorders code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in disorders of pulp and periapical tissues. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

7.1 Pulp and Periapical Conditions:
- K04.0: Pulpitis
- K04.01: Reversible pulpitis
- K04.02: Irreversible pulpitis
- K04.1: Necrosis of pulp
- K04.2: Pulp degeneration
- K04.3: Abnormal hard tissue formation in pulp
- K04.4: Acute apical periodontitis of pulpal origin
- K04.5: Chronic apical periodontitis
- K04.6: Periapical abscess with sinus
- K04.7: Periapical abscess without sinus
- K04.8: Radicular cyst
- K04.9: Other and unspecified diseases of pulp and periapical tissues

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_pulp_periapical_disorders_code(scenario, temperature=0.0):
    """
    Extract pulp and periapical disorders code(s) for a given scenario.
    """
    try:
        chain = create_pulp_periapical_disorders_extractor(temperature)
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
        print(f"Error in extract_pulp_periapical_disorders_code: {str(e)}")
        return ""

def activate_pulp_periapical_disorders(scenario):
    """
    Activate pulp and periapical disorders analysis and return results.
    """
    try:
        return extract_pulp_periapical_disorders_code(scenario)
    except Exception as e:
        print(f"Error in activate_pulp_periapical_disorders: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with severe tooth pain and diagnosis confirms irreversible pulpitis."
    result = activate_pulp_periapical_disorders(scenario)
    print(result)
