"""
Module for extracting trauma and related conditions ICD-10 codes.
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
 
def create_trauma_conditions_extractor(temperature=0.0):
    """
    Create a LangChain-based trauma and related conditions code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in trauma and related conditions. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

16.1 Dislocation and Fracture of Jaw:
- S02.60XA: Fracture of mandible, unspecified, initial encounter
- S02.609A: Fracture of mandible, unspecified part, unspecified side, initial encounter
- S02.61XA: Fracture of condylar process of mandible, initial encounter
- S02.62XA: Fracture of subcondylar process of mandible, initial encounter
- S02.63XA: Fracture of coronoid process of mandible, initial encounter
- S02.64XA: Fracture of ramus of mandible, initial encounter
- S02.65XA: Fracture of angle of mandible, initial encounter
- S02.66XA: Fracture of symphysis of mandible, initial encounter
- S02.67XA: Fracture of alveolus of mandible, initial encounter
- S02.69XA: Fracture of mandible of other specified site, initial encounter
- S03.0XXA: Dislocation of jaw, initial encounter

16.2 Dental Trauma:
- S02.5XXA: Fracture of tooth (traumatic), initial encounter
- S03.2XXA: Dislocation of tooth, initial encounter

16.3 Trauma to Mouth, Oral Cavity, and Related Structures:
- S00.501A: Unspecified superficial injury of lip, initial encounter
- S00.511A: Abrasion of lip, initial encounter
- S00.521A: Blister (nonthermal) of lip, initial encounter
- S00.531A: Contusion of lip, initial encounter
- S00.541A: External constriction of part of lip, initial encounter
- S00.551A: Superficial foreign body of lip, initial encounter
- S00.561A: Insect bite (nonvenomous) of lip, initial encounter
- S00.571A: Other superficial bite of lip, initial encounter
- S00.511A: Abrasion of oral cavity, initial encounter
- S00.512A: Abrasion of oral cavity, initial encounter
- S01.501A: Unspecified open wound of lip, initial encounter
- S01.502A: Unspecified open wound of oral cavity, initial encounter
- S01.511A: Laceration without foreign body of lip, initial encounter
- S01.512A: Laceration without foreign body of oral cavity, initial encounter
- S01.521A: Laceration with foreign body of lip, initial encounter
- S01.522A: Laceration with foreign body of oral cavity, initial encounter
- S01.531A: Puncture wound without foreign body of lip, initial encounter
- S01.532A: Puncture wound without foreign body of oral cavity, initial encounter
- S01.541A: Puncture wound with foreign body of lip, initial encounter
- S01.542A: Puncture wound with foreign body of oral cavity, initial encounter
- S01.551A: Open bite of lip, initial encounter
- S01.552A: Open bite of oral cavity, initial encounter
- S01.90XA: Unspecified open wound of unspecified part of head, initial encounter

16.4 Burns and Corrosions:
- T28.0XXA: Burn of mouth and pharynx, initial encounter
- T28.5XXA: Corrosion of mouth and pharynx, initial encounter

16.5 Foreign Body in Mouth:
- T18.0XXA: Foreign body in mouth, initial encounter
- T18.1XXA: Foreign body in esophagus, initial encounter

16.6 Tongue Injuries:
- S00.532A: Contusion of oral cavity, initial encounter
- S01.512A: Laceration without foreign body of oral cavity, initial encounter
- S01.522A: Laceration with foreign body of oral cavity, initial encounter
- S01.532A: Puncture wound without foreign body of oral cavity, initial encounter
- S01.542A: Puncture wound with foreign body of oral cavity, initial encounter
- S01.552A: Open bite of oral cavity, initial encounter

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_trauma_conditions_code(scenario, temperature=0.0):
    """
    Extract trauma and related conditions code(s) for a given scenario.
    """
    try:
        chain = create_trauma_conditions_extractor(temperature)
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
        print(f"Error in extract_trauma_conditions_code: {str(e)}")
        return ""

def activate_trauma_conditions(scenario):
    """
    Activate trauma and related conditions analysis and return results.
    """
    try:
        return extract_trauma_conditions_code(scenario)
    except Exception as e:
        print(f"Error in activate_trauma_conditions: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with fractured mandible at the condylar process following a sports injury."
    result = activate_trauma_conditions(scenario)
    print(result)
