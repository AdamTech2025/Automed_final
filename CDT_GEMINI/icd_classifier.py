import os
import logging
from dotenv import load_dotenv
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional, List
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
# Import all ICD topic functions 
from icdtopics.dentalencounters import activate_dental_encounters
from icdtopics.dentalcaries import activate_dental_caries
from icdtopics.disordersofteeth import activate_disorders_of_teeth
from icdtopics.disordersofpulpandperiapicaltissues import activate_pulp_periapical_disorders
from icdtopics.diseasesandconditionsoftheperiodontium import activate_periodontium_disorders
from icdtopics.alveolarridgedisorders import activate_alveolar_ridge_disorders
from icdtopics.findingsofbostteeth import activate_lost_teeth
from icdtopics.developmentdisordersofteethandjaws import activate_developmental_disorders
from icdtopics.treatmentcomplications import activate_treatment_complications
from icdtopics.inflammatoryconditionsofthmucosa import activate_inflammatory_mucosa_conditions
from icdtopics.tmjdiseasesandconditions import activate_tmj_disorders
from icdtopics.breathingspeechandsleepdisorders import activate_breathing_speech_sleep_disorders
from icdtopics.traumaandrelatedconditions import activate_trauma_conditions
from icdtopics.oralneoplasms import activate_oral_neoplasms
from icdtopics.pathologies import activate_pathologies
from icdtopics.medicalfindingsrelatedtodentaltreatment import activate_medical_findings
from icdtopics.socialdeterminants import activate_social_determinants
from icdtopics.symptomsanddisorderspertienttoorthodontiacases import activate_orthodontia_cases

load_dotenv()

class ICDClassifier:
    """Class to handle ICD code classification for dental scenarios"""
    
    # Keep your existing category mappings as class attributes
    ICD_CATEGORY_FUNCTIONS = {
        "1": activate_dental_encounters, "2": activate_dental_caries, "3": activate_disorders_of_teeth,
        "4": activate_pulp_periapical_disorders, "5": activate_periodontium_disorders, 
        "6": activate_alveolar_ridge_disorders, "7": activate_lost_teeth, 
        "8": activate_developmental_disorders, "9": activate_treatment_complications,
        "10": activate_inflammatory_mucosa_conditions, "11": activate_tmj_disorders,
        "12": activate_breathing_speech_sleep_disorders, "13": activate_trauma_conditions,
        "14": activate_oral_neoplasms, "15": activate_pathologies, "16": activate_medical_findings,
        "17": activate_social_determinants, "18": activate_orthodontia_cases
    }

    ICD_CATEGORY_NAMES = {
        "1": "Dental Encounters", "2": "Dental Caries", "3": "Disorders of Teeth",
        "4": "Disorders of Pulp and Periapical Tissues", "5": "Diseases and Conditions of the Periodontium",
        "6": "Alveolar Ridge Disorders", "7": "Findings of Lost Teeth",
        "8": "Developmental Disorders of Teeth and Jaws", "9": "Treatment Complications",
        "10": "Inflammatory Conditions of the Mucosa", "11": "TMJ Diseases and Conditions",
        "12": "Breathing, Speech, and Sleep Disorders", "13": "Trauma and Related Conditions",
        "14": "Oral Neoplasms", "15": "Pathologies", "16": "Medical Findings Related to Dental Treatment",
        "17": "Social Determinants", "18": "Symptoms and Disorders Pertinent to Orthodontia Cases"
    }

    PROMPT_TEMPLATE = """
You are an expert dental coding analyst specializing in ICD-10-CM coding for dental conditions. Analyze the given dental scenario and identify ONLY the most appropriate ICD-10-CM code category.

# IMPORTANT INSTRUCTIONS:
- Focus on identifying the SINGLE most relevant category that best represents the primary clinical finding or condition
- Do NOT list multiple categories unless absolutely necessary for complete coding
- Prioritize specificity over breadth - choose the most detailed category that fits the scenario

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

Identify only the most relevant category and provide:

EXPLANATION: [Brief explanation for why this category(s) and code are the most appropriate]
DOUBT: [Any uncertainties,doubts]
CATEGORY: [Category Number and Name, e.g., "2. Dental Caries"]

"""

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

    def _parse_category_response(self, response: str) -> Dict[str, Any]:
        """Parse the initial category classification response"""
        categories, code_lists, explanations, doubts, category_numbers, all_icd_codes = [], [], [], [], [], []
        
        for section in [s for s in response.split("CATEGORY:") if s.strip()]:
            lines = section.strip().split('\n')
            
            category = lines[0].strip()
            if category.startswith(tuple(f"{i}." for i in range(1, 19))):
                category_number = category.split(".", 1)[0].strip()
                category_numbers.append(category_number)
                self.logger.info(f"Found ICD Category: {category_number} - {self.ICD_CATEGORY_NAMES.get(category_number, 'Unknown')}")
            else:
                continue
            
            current_section = None
            codes, explanation, doubt = [], "", ""
            
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                    
                if line == "CODES:":
                    current_section = "codes"
                elif line == "EXPLANATION:":
                    current_section = "explanation"
                elif line == "DOUBT:":
                    current_section = "doubt"
                elif current_section == "codes":
                    codes.append(line)
                    if line and not line.isspace():
                        all_icd_codes.append(line)
                elif current_section == "explanation":
                    explanation = explanation + "\n" + line if explanation else line
                elif current_section == "doubt":
                    doubt = doubt + "\n" + line if doubt else line
            
            categories.append(category)
            code_lists.append(codes)
            explanations.append(explanation)
            doubts.append(doubt)
            
        return {
            "categories": categories,
            "code_lists": code_lists,
            "explanations": explanations,
            "doubts": doubts,
            "category_numbers": category_numbers,
            "all_icd_codes": all_icd_codes
        }

    def _activate_topic(self, category_num: str, scenario: str) -> Dict[str, Any]:
        """Activate and process a specific ICD topic"""
        try:
            activation_function = self.ICD_CATEGORY_FUNCTIONS[category_num]
            category_name = self.ICD_CATEGORY_NAMES[category_num]
            
            self.logger.info(f"Activating: {category_name} (Category {category_num})")
            
            activation_result = activation_function(scenario)
            parsed_result = self._parse_activation_result(activation_result)
            
            return {
                "name": category_name,
                "result": activation_result,
                "parsed_result": parsed_result
            }
        except Exception as e:
            self.logger.error(f"Error activating category {category_num}: {str(e)}")
            return {
                "name": self.ICD_CATEGORY_NAMES.get(category_num, "Unknown"),
                "result": f"Error: {str(e)}",
                "parsed_result": {"error": str(e)}
            }

    def _parse_activation_result(self, result: str) -> Dict[str, Any]:
        """Parse the activation result into structured format"""
        parsed_result = {}
        
        if isinstance(result, str):
            for line in result.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if any(line.startswith(prefix) for prefix in ["- **CODE:**", "**CODE:**", "- CODE:", "CODE:"]):
                    parsed_result["code"] = line.split(":", 1)[1].strip().strip('*')
                elif any(line.startswith(prefix) for prefix in ["- **EXPLANATION:**", "**EXPLANATION:**", "- EXPLANATION:", "EXPLANATION:"]):
                    parsed_result["explanation"] = line.split(":", 1)[1].strip().strip('*')
                elif any(line.startswith(prefix) for prefix in ["- **DOUBT:**", "**DOUBT:**", "- DOUBT:", "DOUBT:"]):
                    parsed_result["doubt"] = line.split(":", 1)[1].strip().strip('*')
        
        return parsed_result

    def process(self, scenario: str) -> Dict[str, Any]:
        """Process a dental scenario and return ICD classifications"""
        try:
            self.logger.info("Starting ICD Classification")
            
            # Get initial classification
            formatted_prompt = self.format_prompt(scenario)
            response = generate_response(formatted_prompt)
            parsed_response = self._parse_category_response(response)
            
            # Process the primary category
            icd_topics_results = {}
            if parsed_response["category_numbers"]:
                primary_category_num = parsed_response["category_numbers"][0]
                if primary_category_num in self.ICD_CATEGORY_FUNCTIONS:
                    icd_topics_results[primary_category_num] = self._activate_topic(
                        primary_category_num, scenario
                    )
            
            result = {
                "categories": parsed_response["categories"],
                "code_lists": parsed_response["code_lists"],
                "explanations": parsed_response["explanations"],
                "doubts": parsed_response["doubts"],
                "category_numbers_string": ",".join(parsed_response["category_numbers"]),
                "icd_topics_results": icd_topics_results,
                "icd_codes": parsed_response["all_icd_codes"]
            }
            
            self.logger.info("ICD Classification Completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in process: {str(e)}")
            return {
                "error": str(e),
                "categories": [],
                "code_lists": [],
                "explanations": [],
                "doubts": [],
                "category_numbers_string": "",
                "icd_topics_results": {},
                "icd_codes": []
            }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class ICDClassifierCLI:
    """Command Line Interface for the ICDClassifier"""
    
    def __init__(self):
        self.classifier = ICDClassifier()

    def print_settings(self):
        """Print current model settings"""
        settings = self.classifier.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print classification results in a formatted way"""
        if "error" in result:
            print(f"\nError: {result['error']}")
            return

        print("\n=== ICD-10-CM CATEGORIES IDENTIFIED ===")
        if not result["categories"]:
            print("No ICD categories were identified for this scenario.")
        else:
            for i, category in enumerate(result["categories"]):
                print(f"\nCategory {i+1}: {category}")
                if result["code_lists"][i]:
                    print("CODES:")
                    for code in result["code_lists"][i]:
                        if code and not code.isspace():
                            print(f"  {code}")
                else:
                    print("CODES: None specified")
                    
                if result["explanations"][i]:
                    print("EXPLANATION:")
                    print(result["explanations"][i])
                
                if result["doubts"][i]:
                    print("DOUBT:")
                    print(result["doubts"][i])
                print("-" * 50)

        print("\n=== ICD TOPICS ACTIVATION RESULTS ===")
        if result["icd_topics_results"]:
            for category_num, topic_data in result["icd_topics_results"].items():
                print(f"\nCategory {category_num}: {topic_data['name']}")
                print(f"Activation Result:")
                print(topic_data['result'])
                
                if "parsed_result" in topic_data:
                    parsed = topic_data["parsed_result"]
                    print("\nParsed Data:")
                    for key, value in parsed.items():
                        print(f"{key.title()}: {value}")
                print("-" * 50)
        else:
            print("No ICD topics were activated for this scenario.")

        print("\n=== SUMMARY ===")
        print(f"Total categories identified: {len(result['categories'])}")
        print(f"Total ICD codes found: {len(result['icd_codes'])}")
        if result['icd_codes']:
            print("Codes found:")
            for code in result['icd_codes']:
                print(f"  - {code}")
        print(f"Categories activated: {result['category_numbers_string'] or 'None'}")

    def run(self):
        """Run the CLI interface"""
        self.print_settings()
        default_scenario = "A 32-year-old female patient is currently nicotine dependent..."  # Your default scenario
        scenario = input("Enter a dental scenario to classify (or press Enter for default): ") or default_scenario
        result = self.classifier.process(scenario)
        self.print_results(result)

def main():
    """Main entry point for the script"""
    cli = ICDClassifierCLI()
    cli.run()

if __name__ == "__main__":
    main()