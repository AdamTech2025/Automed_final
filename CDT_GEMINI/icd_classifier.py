import os
import logging
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional, List
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP

load_dotenv()

class ICDClassifier:
    """Class to handle *initial* ICD code category classification for dental scenarios"""

    PROMPT_TEMPLATE = """
You are an expert dental coding analyst specializing in ICD-10-CM coding for dental conditions. Analyze the given dental scenario and identify ONLY the single most appropriate ICD-10-CM code category number and provide a brief explanation.

# IMPORTANT INSTRUCTIONS:
- Focus on identifying the SINGLE most relevant category number that best represents the primary clinical finding or condition.
- Prioritize specificity over breadth - choose the most detailed category that fits the scenario.
- ONLY output the Category Number, Explanation, and Doubt using the specified format.

# ICD-10-CM CATEGORIES RELEVANT TO DENTISTRY:
1. Dental Encounters (Z01.2x series: routine dental examinations)
2. Dental Caries (K02.x series: including different sites, severity, and stages)
3. Disorders of Teeth (K03.x-K08.x series: wear, deposits, embedded/impacted teeth)
4. Disorders of Pulp and Periapical Tissues (K04.x series: pulpitis, necrosis, abscess)
5. Diseases and Conditions of the Periodontium (K05.x-K06.x series: gingivitis, periodontitis)
6. Alveolar Ridge Disorders (K08.2x series: atrophy, specific disorders)
7. Findings of Lost Teeth (K08.1x, K08.4x series: loss due to extraction, trauma)
8. Developmental Disorders of Teeth and Jaws (K00.x, K07.x series: anodontia, malocclusion)
9. Treatment Complications (T81.x-T88.x series: infection, dehiscence, foreign body)
10. Inflammatory Conditions of the Mucosa (K12.x series: stomatitis, cellulitis)
11. TMJ Diseases and Conditions (M26.6x series: disorders, adhesions, arthralgia)
12. Breathing, Speech, and Sleep Disorders (G47.x, F80.x, R06.x series: relevant to dental)
13. Trauma and Related Conditions (S00.x-S09.x series: injuries to mouth, teeth, jaws)
14. Oral Neoplasms (C00.x-C14.x series: malignant neoplasms of lip, oral cavity)
15. Pathologies (D10.x-D36.x series: benign neoplasms, cysts, conditions)
16. Medical Findings Related to Dental Treatment (E08.x-E13.x for diabetes, I10-I15 for hypertension)
17. Social Determinants (Z55.x-Z65.x series: education, housing, social factors)
18. Symptoms and Disorders Pertinent to Orthodontia Cases (G24.x, G50.x, M95.x: facial asymmetry)

# SCENARIO TO ANALYZE:
{scenario}

# STRICT OUTPUT FORMAT - FOLLOW EXACTLY:
CATEGORY_NUMBER: [Provide only the single most relevant category number, e.g., 4]
EXPLANATION: [Brief explanation for why this category number is the most appropriate]
DOUBT: [Any uncertainties or doubts about the category selection]
""" # Simplified prompt

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the classifier with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the classifier module"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def configure(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        """Configure model and temperature settings"""
        if model:
            set_model(model)
        if temperature is not None:
            set_temperature(temperature)

    def format_prompt(self, scenario: str) -> str:
        """Format the prompt template with the given scenario"""
        return self.PROMPT_TEMPLATE.format(scenario=scenario)

    def _parse_initial_classification(self, response: str) -> Dict[str, Any]:
        """Parse the initial category classification response (category number, explanation, doubt)."""
        category_number = None
        explanation = None
        doubt = None
        
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("CATEGORY_NUMBER:"):
                category_number = line.split(":", 1)[1].strip()
            elif line.startswith("EXPLANATION:"):
                explanation = line.split(":", 1)[1].strip()
            elif line.startswith("DOUBT:"):
                doubt = line.split(":", 1)[1].strip()
                
        # Basic validation
        if category_number and category_number.isdigit() and 1 <= int(category_number) <= 18:
             self.logger.info(f"Parsed initial classification: Category Number={category_number}")
             return {
                "category_number": category_number,
                "explanation": explanation,
                "doubt": doubt,
                "raw_data": response # Include raw response here
            }
        else:
             self.logger.warning(f"Could not parse valid category number from response: {response}")
             return { # Return structure indicating parsing failure
                "category_number": None,
                "explanation": "Failed to parse category number from LLM response.",
                "doubt": response, # Include raw response in doubt for debugging
                "raw_data": response # Include raw response here too
            }

    def process(self, scenario: str) -> Dict[str, Any]: # Return type is now Dict
        """Process a dental scenario to get the initial ICD category classification."""
        raw_response = ""
        try:
            self.logger.info("Starting Initial ICD Category Classification")
            formatted_prompt = self.format_prompt(scenario)
            raw_response = generate_response(formatted_prompt) # Store raw response
            parsed_response = self._parse_initial_classification(raw_response)
            
            self.logger.info("Initial ICD Category Classification Completed")
            # Return the dictionary directly
            return parsed_response 

        except Exception as e:
            self.logger.error(f"Error in Initial ICD process: {str(e)}")
            # Return error structure including raw response if available
            return {
                "category_number": None,
                "explanation": f"An error occurred during initial ICD classification: {str(e)}",
                "doubt": "Processing could not be completed.",
                "raw_data": raw_response, # Include raw response in error case
                "error": str(e)
            }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }