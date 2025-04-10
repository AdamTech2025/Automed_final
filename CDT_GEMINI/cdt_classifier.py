import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file


load_dotenv()

# You can set a specific model for this file only
# Uncomment and modify the line below to use a specific model
# set_model_for_file("gemini-1.5-pro")




def create_cdt_classifier(temperature=0.0):
    # Create the prompt template
    prompt_template = PromptTemplate(
        template="""
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


STRICT OUTPUT FORMAT - FOLLOW EXACTLY:

For each code range, you must use the following format, with no additional text:

CODE_RANGE: D0100-D0999 - Diagnostic Services

EXPLANATION:
[Provide a detailed explanation for why this code range was selected, with specific references to the scenario elements]

DOUBT:
[List any uncertainties or alternative interpretations that might affect code selection, or ask a question here if you need more data to be sure]

CODE_RANGE: D0100-D0999 - Diagnostic Services

Repeat this exact format for each relevant code range. Do not add additional text, comments, or summaries outside of this format.
        """,
        input_variables=["scenario"]
    )
    
    # Create the chain using our LLM service
    return create_chain(prompt_template)

def classify_cdt_categories(scenario, temperature=0.0):
    # Use the already cleaned scenario directly
    processed_scenario = scenario
    
    # Then classify it - rely on the LLM's analysis rather than keyword detection
    chain = create_cdt_classifier(temperature)
    result = invoke_chain(chain, {"scenario": processed_scenario})["text"].strip()
    
    # This will hold just the range codes for API usage
    range_codes = []
    explanations = []
    doubts = []
    
    # Split the result by "CODE_RANGE:" to get each section
    sections = result.split("CODE_RANGE:")
    
    # Skip the first empty section if it exists
    sections = [s for s in sections if s.strip()]
    
    for section in sections:
        lines = section.strip().split('\n')
        
        # First line should be the code range
        if not lines:
            continue
            
        code_range_line = lines[0].strip()
        
        # Extract CDT code range (e.g., "D0100-D0999")
        if " - " in code_range_line:
            code_parts = code_range_line.split(" - ")
            if code_parts and code_parts[0].strip().startswith("D"):
                range_code = code_parts[0].strip()
                
                # Initialize variables for the current section
                explanation = ""
                doubt = ""
                current_section = None
                
                # Process the remaining lines to extract explanation and doubt
                for line in lines[1:]:
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    if line == "EXPLANATION:":
                        current_section = "explanation"
                    elif line == "DOUBT:":
                        current_section = "doubt"
                    elif current_section == "explanation":
                        if explanation:
                            explanation += "\n" + line
                        else:
                            explanation = line
                    elif current_section == "doubt":
                        if doubt:
                            doubt += "\n" + line
                        else:
                            doubt = line
                
                # Only add to results if we have a valid code range
                range_codes.append(range_code)
                explanations.append(explanation)
                doubts.append(doubt)
    
    # Create a comma-separated string of just the range codes
    range_codes_string = ",".join(range_codes)
    
    # Create the formatted results
    formatted_results = []
    for i, range_code in enumerate(range_codes):
        formatted_results.append({
            "code_range": range_code,
            "explanation": explanations[i] if i < len(explanations) else "",
            "doubt": doubts[i] if i < len(doubts) else ""
        })
    
    # Return the formatted results and the range codes string
    return {
        "formatted_results": formatted_results,
        "range_codes_string": range_codes_string
    }


# For testing if run directly
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    test_scenario = input("Enter a dental scenario to classify: ")
    result = classify_cdt_categories(test_scenario)
    
    print("\n=== CDT CODE RANGES ===")
    for item in result["formatted_results"]:
        print(f"CODE RANGE: {item['code_range']}")
        print(f"EXPLANATION: {item['explanation']}")
        print(f"DOUBT: {item['doubt']}")
        print("-" * 50)
    
    print(f"\nRange Codes String: {result['range_codes_string']}")