import os
import logging
import sys
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

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

# Load environment variables and setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# You can set a specific model for this file only
# Uncomment and modify the line below to use a specific model
# set_model_for_file("gemini-1.5-pro")

# Maps of ICD categories to functions and names
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

def classify_icd_categories(scenario, temperature=0.0):
    """Classify a dental scenario into the single most appropriate ICD-10-CM category and activate only that topic function"""
    logger.info("Starting ICD Classification")
    
    # Create prompt for classification
    prompt_template = PromptTemplate(
        template="""
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

        """,
        input_variables=["scenario"]
    )
    
    # Get initial classification from LLM
    llm_service = get_llm_service()
    logger.info(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    # Create the chain using LLM service
    chain = create_chain(prompt_template)
    result = invoke_chain(chain, {"scenario": scenario})["text"].strip()
    
    # Parse results
    categories, code_lists, explanations, doubts, category_numbers, all_icd_codes = [], [], [], [], [], []
    
    # Extract sections from result
    for section in [s for s in result.split("CATEGORY:") if s.strip()]:
        lines = section.strip().split('\n')
        
        # Get category
        category = lines[0].strip()
        if category.startswith(tuple(f"{i}." for i in range(1, 19))):
            category_number = category.split(".", 1)[0].strip()
            category_numbers.append(category_number)
            logger.info(f"Found ICD Category: {category_number} - {ICD_CATEGORY_NAMES.get(category_number, 'Unknown')}")
        else:
            # Skip malformed categories
            continue
        
        # Extract codes, explanation and doubt
        current_section = None
        codes, explanation, doubt = [], "", ""
        
        for line in lines[1:]:
            line = line.strip()
            if not line: continue
                
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
        
        # Add to collections
        categories.append(category)
        code_lists.append(codes)
        explanations.append(explanation)
        doubts.append(doubt)
    
    # Only process the first category (most relevant one)
    icd_topics_results = {}
    if category_numbers:
        # Take only the first category identified (most relevant per our prompt)
        primary_category_num = category_numbers[0]
        logger.info(f"Processing only the primary category: {primary_category_num} - {ICD_CATEGORY_NAMES.get(primary_category_num, 'Unknown')}")
        
        if primary_category_num in ICD_CATEGORY_FUNCTIONS:
            activation_function = ICD_CATEGORY_FUNCTIONS[primary_category_num]
            category_name = ICD_CATEGORY_NAMES[primary_category_num]
            
            logger.info(f"Activating: {category_name} (Category {primary_category_num})")
            
            try:
                # Call the activation function with the scenario parameter
                activation_result = activation_function(scenario)
                
                # Parse the result
                parsed_result = {}
                
                if isinstance(activation_result, str):
                    for line in activation_result.split('\n'):
                        line = line.strip()
                        if not line: continue
                        
                        if any(line.startswith(prefix) for prefix in ["- **CODE:**", "**CODE:**", "- CODE:", "CODE:"]):
                            parsed_result["code"] = line.replace("- **CODE:**", "").replace("**CODE:**", "").replace("- CODE:", "").replace("CODE:", "").strip()
                        elif any(line.startswith(prefix) for prefix in ["- **EXPLANATION:**", "**EXPLANATION:**", "- EXPLANATION:", "EXPLANATION:"]):
                            parsed_result["explanation"] = line.replace("- **EXPLANATION:**", "").replace("**EXPLANATION:**", "").replace("- EXPLANATION:", "").replace("EXPLANATION:", "").strip()
                        elif any(line.startswith(prefix) for prefix in ["- **DOUBT:**", "**DOUBT:**", "- DOUBT:", "DOUBT:"]):
                            parsed_result["doubt"] = line.replace("- **DOUBT:**", "").replace("**DOUBT:**", "").replace("- DOUBT:", "").replace("DOUBT:", "").strip()
                
                # Extract codes from activation result if found
                if "code" in parsed_result and parsed_result["code"] and not parsed_result["code"].isspace():
                    code_text = parsed_result["code"]
                    if code_text not in all_icd_codes:
                        all_icd_codes.append(code_text)
                
                # Store results
                icd_topics_results[primary_category_num] = {
                    "name": category_name,
                    "result": activation_result,
                    "parsed_result": parsed_result
                }
            except Exception as e:
                logger.error(f"Error activating {category_name}: {str(e)}")
                icd_topics_results[primary_category_num] = {
                    "name": category_name,
                    "result": f"Error: {str(e)}",
                    "parsed_result": {"error": str(e)}
                }
    else:
        logger.warning("No valid ICD categories were identified")
    
    logger.info("ICD Classification Completed")
    
    return {
        "categories": categories,
        "code_lists": code_lists,
        "explanations": explanations,
        "doubts": doubts,
        "category_numbers_string": ",".join(category_numbers),
        "icd_topics_results": icd_topics_results,
        "icd_codes": all_icd_codes
    }

if __name__ == "__main__":
    print("=== ICD-10-CM CLASSIFIER TEST ===")
    print("This will test both the classifier and topic activation functions")
    
    # Get a complete dental scenario - provide default if running tests
    default_scenario = "A 32-year-old female patient is currently nicotine dependent, smoking one pack of cigarettes per day. She has had multiple failed attempts at quitting using nicotine gum. Approximately 10 minutes were spent counseling the patient in cessation techniques."
    
    # Check for command line arguments first
    if len(sys.argv) > 1:
        test_scenario = " ".join(sys.argv[1:])
    else:
        test_scenario = input(f"Enter a dental scenario to classify (or press Enter for default scenario): ") or default_scenario
    
    print(f"\nAnalyzing scenario: {test_scenario}\n")
    print("Processing...")
    
    # Run the classifier
    result = classify_icd_categories(test_scenario)
    
    # Display the identified categories
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
    
    # Display the activation results from topic files
    print("\n=== ICD TOPICS ACTIVATION RESULTS ===")
    if result["icd_topics_results"]:
        for category_num, topic_data in result["icd_topics_results"].items():
            print(f"\nCategory {category_num}: {topic_data['name']}")
            print(f"Activation Result:")
            
            if isinstance(topic_data['result'], str) and topic_data['result'].startswith("Error:"):
                print(f"⚠️ {topic_data['result']}")
            else:
                print(f"{topic_data['result']}")
            
            if "parsed_result" in topic_data and topic_data["parsed_result"]:
                parsed = topic_data["parsed_result"]
                print("\nParsed Data:")
                if "code" in parsed and parsed["code"]:
                    print(f"Code: {parsed['code']}")
                else:
                    print("Code: None specified")
                    
                if "explanation" in parsed and parsed["explanation"]:
                    print(f"Explanation: {parsed['explanation']}")
                    
                if "doubt" in parsed and parsed["doubt"]:
                    print(f"Doubt: {parsed['doubt']}")
                    
                if "error" in parsed and parsed["error"]:
                    print(f"Error: {parsed['error']}")
            print("-" * 50)
    else:
        print("No ICD topics were activated for this scenario.")
    
    # Summary statistics
    print("\n=== SUMMARY ===")
    print(f"Total categories identified: {len(result['categories'])}")
    print(f"Total ICD codes found: {len(result['icd_codes'])}")
    if result['icd_codes']:
        print("Codes found:")
        for code in result['icd_codes']:
            print(f"  - {code}")
    print(f"Categories activated: {result['category_numbers_string'] or 'None'}")
    print("=== TEST COMPLETE ===") 