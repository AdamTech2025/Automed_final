"""
Module for extracting breathing, speech, and sleep disorders ICD-10 codes.
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
 
def create_breathing_speech_sleep_disorders_extractor(temperature=0.0):
    """
    Create a LangChain-based breathing, speech, and sleep disorders code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in breathing, speech, and sleep disorders. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Breathing, Speech, and Sleep Disorders ICD-10 codes include:
12.1 Mouthbreathing
- R06.5: Mouth breathing
- R06.83: Snoring
- R06.89: Other abnormalities of breathing

12.2 Speech Disorders
- R47.9: Unspecified speech disturbances
- F80.89: Other developmental disorders of speech and language
- F80.9: Developmental disorder of speech and language, unspecified

12.3 Sleep-Related Breathing Disorders
- G47.30: Sleep apnea, unspecified
- G47.31: Primary central sleep apnea
- G47.32: High altitude periodic breathing
- G47.33: Obstructive sleep apnea (adult) (pediatric)
- G47.34: Idiopathic sleep-related nonobstructive alveolar hypoventilation
- G47.35: Congenital central alveolar hypoventilation syndrome
- G47.36: Sleep-related hypoventilation in conditions classified elsewhere
- G47.37: Central sleep apnea in conditions classified elsewhere
- G47.39: Other sleep apnea
- G47.63: Sleep-related bruxism
- G47.8: Other sleep disorders
- G47.9: Sleep disorder, unspecified

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_breathing_speech_sleep_disorders_code(scenario, temperature=0.0):
    """
    Extract breathing, speech, and sleep disorders code(s) for a given scenario.
    """
    try:
        chain = create_breathing_speech_sleep_disorders_extractor(temperature)
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
        print(f"Error in extract_breathing_speech_sleep_disorders_code: {str(e)}")
        return ""

def activate_breathing_speech_sleep_disorders(scenario):
    """
    Activate breathing, speech, and sleep disorders analysis and return results.
    """
    try:
        return extract_breathing_speech_sleep_disorders_code(scenario)
    except Exception as e:
        print(f"Error in activate_breathing_speech_sleep_disorders: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient diagnosed with obstructive sleep apnea following a sleep study."
    result = activate_breathing_speech_sleep_disorders(scenario)
    print(result)
