"""
Module for extracting TMJ diseases and conditions ICD-10 codes.
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
 
def create_tmj_disorders_extractor(temperature=0.0):
    """
    Create a LangChain-based TMJ diseases and conditions code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in TMJ diseases and conditions. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

11.1 TMJ Disorders:
- M26.601: Right temporomandibular joint disorder, unspecified
- M26.602: Left temporomandibular joint disorder, unspecified
- M26.603: Bilateral temporomandibular joint disorder, unspecified
- M26.609: Unspecified temporomandibular joint disorder, unspecified side
- M26.69: Other specified disorders of temporomandibular joint

11.2 Adhesions and Ankylosis:
- M26.611: Adhesions and ankylosis of right temporomandibular joint
- M26.612: Adhesions and ankylosis of left temporomandibular joint
- M26.613: Adhesions and ankylosis of bilateral temporomandibular joint

11.3 Arthralgia:
- M26.621: Arthralgia of right temporomandibular joint
- M26.622: Arthralgia of left temporomandibular joint
- M26.623: Arthralgia of bilateral temporomandibular joint

11.4 Articular Disc Disorders:
- M26.631: Articular disc disorder of right temporomandibular joint
- M26.632: Articular disc disorder of left temporomandibular joint
- M26.633: Articular disc disorder of bilateral temporomandibular joint

11.5 Arthritis of Temporomandibular Joint:
- M26.641: Arthritis of right temporomandibular joint
- M26.642: Arthritis of left temporomandibular joint
- M26.643: Arthritis of bilateral temporomandibular joint

11.6 Arthropathy of Temporomandibular Joint:
- M26.651: Arthropathy of right temporomandibular joint
- M26.652: Arthropathy of left temporomandibular joint
- M26.653: Arthropathy of bilateral temporomandibular joint

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_tmj_disorders_code(scenario, temperature=0.0):
    """
    Extract TMJ diseases and conditions code(s) for a given scenario.
    """
    try:
        chain = create_tmj_disorders_extractor(temperature)
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
        print(f"Error in extract_tmj_disorders_code: {str(e)}")
        return ""

def activate_tmj_disorders(scenario):
    """
    Activate TMJ diseases and conditions analysis and return results.
    """
    try:
        return extract_tmj_disorders_code(scenario)
    except Exception as e:
        print(f"Error in activate_tmj_disorders: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with arthralgia of the left temporomandibular joint."
    result = activate_tmj_disorders(scenario)
    print(result)
