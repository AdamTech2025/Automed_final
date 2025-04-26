import os
import logging
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import generate_response, get_service, set_model, set_temperature
from typing import Dict, Any, Optional, List
from llm_services import OPENROUTER_MODEL, DEFAULT_TEMP
import re

load_dotenv()

class CDTClassifier:
    """Class to handle CDT code classification for dental scenarios"""
    
    PROMPT_TEMPLATE = """
    I. D0100-D0999 - Diagnostic Services This range includes all diagnostic procedures necessary to evaluate a patient's oral health status. It covers:
    Comprehensive and periodic oral evaluations (routine check-ups, new patient exams).
    Problem-focused and limited evaluations for emergencies or specific concerns.
    Radiographic imaging including bitewings, panoramic, periapical, and full-mouth series.
    Diagnostic tests for pulp vitality and caries susceptibility (e.g., electric pulp testing).
    Clinical data collection for diagnosis and treatment planning.
    Important for initial visits, emergency walk-ins, and routine recall visits.

    II. D1000-D1999 - Preventive Services This range focuses on preventing oral diseases and maintaining oral health. It includes:
    Dental cleanings (prophylaxis) for children and adults.
    Fluoride treatments (varnish, gels) to strengthen enamel and prevent decay.
    Application of sealants to prevent decay in pits and fissures of molars.
    Oral hygiene instructions and tobacco/nutritional counseling.
    Preventive resin restorations.
    Space maintainers for pediatric patients.
    Best used in pediatric and routine hygiene appointments.

    III. D2000-D2999 - Restorative Services Covers procedures for restoring damaged teeth to proper form and function. This includes:
    Direct restorations: amalgam and composite (tooth-colored) fillings.
    Indirect restorations: inlays, onlays, crowns.
    Crown buildup with core and posts after root canals.
    Prefabricated crowns (e.g., stainless steel crowns in pediatric cases).
    Repairs to restorations and recementation of crowns and bridges.
    Typically used after decay removal or trauma.

    IV. D3000-D3999 - Endodontic Services These codes pertain to the treatment of the dental pulp and tissues surrounding the root. They include:
    Pulp capping (direct and indirect).
    Pulpotomy for primary teeth.
    Root canal therapy for anterior, bicuspid, and molar teeth.
    Retreatment of previous root canals.
    Apicoectomy and periradicular surgery.
    Therapeutic pulpal procedures for maintaining vitality.
    Crucial for patients experiencing severe pain, infection, or abscesses.

    V. D4000-D4999 - Periodontic Services Involves treatment of the supporting structures of the teeth (gums and bone). This includes:
    Non-surgical procedures: scaling and root planing, periodontal maintenance.
    Surgical procedures: gingivectomy, flap surgery, osseous surgery, crown lengthening.
    Management of periodontal disease and bone loss.
    Localized antimicrobial delivery.
    Used when treating gingivitis or periodontitis.

    VI. D5000-D5899 - Prosthodontics, Removable Covers services for removable tooth replacement appliances. Includes:
    Complete and partial dentures (initial fabrication).
    Interim prostheses for temporary restoration.
    Adjustments, relining, rebasing of existing dentures.
    Repairs to removable prostheses.
    Usually used in elderly patients or those with multiple missing teeth.

    VII. D5900-D5999 - Maxillofacial Prosthetics These are specialized prosthetics for anatomical restoration. Services include:
    Obturators for cleft palate or surgical defects.
    Speech aids, feeding aids, and radiation carriers.
    Ocular and facial prosthetics.
    Used mostly in conjunction with oral surgeons, ENT, or oncology cases.

    VIII. D6000-D6199 - Implant Services All services involving dental implants are coded here. These include:
    Pre-implant diagnostics and treatment planning.
    Surgical placement of implants.
    Post-surgical maintenance of implants.
    Restoration procedures like implant crowns, abutments, and overdentures.
    Necessary in cases of missing teeth, particularly when fixed prosthetics are preferred.

    IX. D6200-D6999 -Prosthodontics, Fixed These codes are for permanent, fixed tooth replacements. Includes:
    Pontics and retainers used in bridges.
    Fixed partial dentures and associated components.
    Precision attachments, stress breakers.
    Repairs or replacement of components.
    Ideal for patients desiring non-removable tooth replacement.

    X. D7000-D7999 - Oral and Maxillofacial Surgery Includes surgical procedures involving the teeth, jaws, and surrounding tissues. Services include:
    Extractions (routine, surgical, or impacted teeth).
    Note: Discussions at the Code Maintenance Committee (CMC) meetings
    indicated that D7510 was considered to be appropriate even when the incision
    is made through the gingival sulcus.
    Alveoloplasty and surgical preparation for prosthetics.
    Biopsy, excision of cysts and lesions.
    Incision and drainage of infections.
    Treatment of facial trauma including fractures and dislocations.
    Required for emergency care, complex tooth removals, and pathological cases.

    XI. D8000-D8999 - Orthodontics Encompasses the diagnosis and correction of misaligned teeth and jaws. Services include:
    Limited and comprehensive orthodontic treatment.
    Minor tooth movement.
    Periodic observation visits.
    Retention and follow-up.
    Best for children, teens, or adults undergoing braces or aligners.

    XII. D9000-D9999 - Adjunctive General Services Miscellaneous services that support or enhance dental care. Includes:
    Anesthesia (local, general, IV sedation).
    Professional consultations and second opinions.
    Drug/medication application.
    Behavior management (for pediatric, anxious, or special needs patients).
    Bleaching for cosmetic purposes.
    Occlusal guards for bruxism.
    Use for sedation dentistry, patient management, and non-treatment-related services.

    SCENARIO TO ANALYZE:
    {scenario}

    Your Task:
    1) Thorough Analysis: Carefully analyze the entire dental scenario provided below.
    2) Maximize Billing Potential: Identify every CDT code range that may be applicable to the procedures mentioned, with a focus on maximizing billable items for the visit.
    3) Ensure Denial-Proof Coding: Your coding must be precise and defensible to avoid any chance of claim denial.
    4) Allow for Extra Ranges: False positives are acceptable and even encouraged, as any extra ranges will later be refined by additional agents but missing codes will not be added and might lead to less revenue or denial.
    5) Independent and Accurate Thinking: While you must strictly use the provided CDT code ranges, allow yourself to think critically about the scenario and include any ranges that might be relevant, even if not directly outlined in the definitions.
    6) Strict Output Structure: For each identified code range, strictly follow the structure below. Do not include any additional text outside of this structure or alter the code ranges provided.

    Important Guidelines:
    1) Only use information provided in the scenario. Do not add or infer any extra details.
    2) Ensure that every detail from the scenario is considered, and include comprehensive explanations for each code range.
    3) Only select from the CDT code ranges provided; do not modify or invent new ranges.
    4) IMPORTANT: Always consider preventive codes (D1000-D1999) when the scenario mentions terms like "prophylaxis", "prophy", "cleaning", or "routine recall exam and prophylaxis". Prophylaxis is a key preventive service commonly performed during routine dental visits.
    5) For restorative procedures, pay careful attention to mention of posts, cores, buildups or similar structures used before crown placement, as these are separate billable services from the crown itself.
    6) CRITICAL: Always consider endodontic codes (D3000-D3999) when the scenario mentions any form of "root canal therapy", "pulpectomy", "pulpotomy", "retreatment", or any treatment related to the dental pulp or periapical tissues.
    7) If there is any mention of a drainage of abscess, incision, or drainage of a fistula, consider oral surgery codes (D7000-D7999).
    8) Remember that radiographic images (x-rays) always fall under diagnostic services (D0100-D0999), regardless of why they were taken.

    STRICT OUTPUT FORMAT - FOLLOW EXACTLY:
    For each code range, you must use the following format, with no additional text:

    CODE_RANGE: D0100-D0999 - Diagnostic Services
    EXPLANATION:
    [Provide a detailed explanation for why this code range was selected, with specific references to the scenario elements]
    DOUBT:
    [List any uncertainties or alternative interpretations that might affect code selection, or ask a question here if you need more data to be sure]

    CODE_RANGE: D0100-D0999 - Diagnostic Services
    Repeat this exact format for each relevant code range. Do not add additional text, comments, or summaries outside of this format.
    """

    def __init__(self, model: str = OPENROUTER_MODEL, temperature: float = DEFAULT_TEMP):
        """Initialize the classifier with model and temperature settings"""
        self.service = get_service()
        self.configure(model, temperature)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the classifier module"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def configure(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        """Configure model and temperature settings"""
        if model:
            set_model(model)
        if temperature is not None:
            set_temperature(temperature)

    def format_prompt(self, scenario: str) -> str:
        """Format the prompt template with the given scenario"""
        return self.PROMPT_TEMPLATE.format(scenario=scenario)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format using regex"""
        formatted_results = []
        range_codes_set = set()

        # Regex to capture each CODE_RANGE block and its contents
        pattern = re.compile(
            r"CODE_RANGE:\s*(D\d{4}-D\d{4})\s*-\s*.*?\n(.*?)(?=CODE_RANGE:|$)",
            re.DOTALL | re.IGNORECASE
        )
        matches = pattern.findall(response)
        
        for match in matches:
            code_range = match[0].strip()
            content = match[1].strip()
            
            explanation = None
            doubt = None

            # Regex to find EXPLANATION within the content block
            exp_match = re.search(r"EXPLANATION:\s*(.*?)(?=DOUBT:|$)", content, re.DOTALL | re.IGNORECASE)
            if exp_match:
                explanation = exp_match.group(1).strip() or None

            # Regex to find DOUBT within the content block
            doubt_match = re.search(r"DOUBT:\s*(.*)", content, re.DOTALL | re.IGNORECASE)
            if doubt_match:
                doubt = doubt_match.group(1).strip() or None

            # Skip if both explanation and doubt are empty
            if explanation or doubt:
                formatted_results.append({
                    "code_range": code_range,
                    "explanation": explanation,
                    "doubt": doubt
                })
                range_codes_set.add(code_range)
            
        self.logger.info(f"Parsed {len(formatted_results)} code ranges using regex.")
        
        return {
            "formatted_results": formatted_results,
            "range_codes_string": ",".join(sorted(list(range_codes_set)))
        }

    def process(self, scenario: str) -> Dict[str, Any]:
        """Process a dental scenario to get CDT classification"""
        raw_response = ""
        try:
            self.logger.info("Starting CDT Classification")
            if not scenario or len(scenario.strip()) == 0:
                raise ValueError("Scenario cannot be empty")
            if len(scenario) > 10000:
                raise ValueError("Scenario is too long")
            
            formatted_prompt = self.format_prompt(scenario)
            raw_response = generate_response(formatted_prompt)
            parsed_response = self.parse_response(raw_response)
            
            self.logger.info("CDT Classification Completed")
            parsed_response['raw_data'] = raw_response
            return parsed_response

        except ValueError as ve:
            self.logger.error(f"Validation error: {str(ve)}")
            return {
                "formatted_results": [],
                "range_codes_string": None,
                "raw_data": raw_response,
                "error": str(ve)
            }
        except Exception as e:
            self.logger.error(f"Error in CDT process: {str(e)}", exc_info=True)
            return {
                "formatted_results": [],
                "range_codes_string": None,
                "raw_data": raw_response,
                "error": str(e)
            }

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current model settings"""
        return {
            "model": self.service.model,
            "temperature": self.service.temperature
        }

class CDTClassifierCLI:
    """Command Line Interface for the CDTClassifier"""
    
    def __init__(self):
        self.classifier = CDTClassifier()

    def print_settings(self):
        """Print current model settings"""
        settings = self.classifier.current_settings
        print(f"Using model: {settings['model']} with temperature: {settings['temperature']}")

    def print_results(self, result: Dict[str, Any]):
        """Print classification results in a formatted way"""
        if "error" in result:
            print(f"\nError: {result['error']}")
            return

        print("\n=== CDT CODE RANGES ===")
        for item in result["formatted_results"]:
            print(f"CODE RANGE: {item['code_range']}")
            print(f"EXPLANATION: {item['explanation']}")
            print(f"DOUBT: {item['doubt']}")
            print("-" * 50)
        print(f"\nRange Codes String: {result['range_codes_string']}")

    def run(self):
        """Run the CLI interface"""
        self.print_settings()
        scenario = input("Enter a dental scenario to classify: ").strip()
        result = self.classifier.process(scenario)
        self.print_results(result)

def main():
    """Main entry point for the script"""
    cli = CDTClassifierCLI()
    cli.run()

if __name__ == "__main__":
    main()