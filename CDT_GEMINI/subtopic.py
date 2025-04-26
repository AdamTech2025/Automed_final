import json
import re
from langchain.prompts import PromptTemplate
import copy

class DentalCodeManager:
    def __init__(self):
        self.name = ""
        self.strict = False
        self.schema = {
            "explanation": "",
            "doubt": "",
            "code_range": "",
            "activated_subtopics": "",
            "specific_codes": []
        }
        # Placeholder for llm_service (commented out since get_service is not provided)
        # self.llm_service = get_service()
        self.parser_prompt = PromptTemplate(
            template="""You are a dental coding expert. Parse the following raw output into a structured format.
Extract all CDT codes (D####), explanations, and any doubts.
If multiple codes are found, include all of them.

Raw Output:
{raw_output}

IMPORTANT: You must respond with ONLY a valid JSON object in exactly this format (no other text):
{{
    "specific_codes": ["D####"],
    "explanation": "clear explanation of why these codes",
    "doubt": "any doubts or None"
}}

Rules:
1. specific_codes must be an array, even for single codes
2. If no codes found, use empty array []
3. Never include line breaks in explanation or doubt
4. Do not include any text outside the JSON object
5. Always include all three fields
""",
            input_variables=["raw_output"]
        )

    def update_values(self, name, strict, explanation, doubt, code_range, activated_subtopics, specific_codes):
        self.name = name
        self.strict = strict
        self.schema["explanation"] = explanation
        self.schema["doubt"] = doubt
        self.schema["code_range"] = code_range
        self.schema["activated_subtopics"] = activated_subtopics
        self.schema["specific_codes"] = specific_codes

    def parse_llm_output(self, raw_output: str) -> list:
        try:
            # First try to parse as JSON if it's already in JSON format
            try:
                if isinstance(raw_output, str):
                    pre_parsed = json.loads(raw_output)
                else:
                    pre_parsed = raw_output
                
                # If it's from diagnostic services, extract codes from topic_result
                if isinstance(pre_parsed, dict) and "topic_result" in pre_parsed:
                    codes = []
                    explanation = []
                    for result in pre_parsed["topic_result"].values():
                        if isinstance(result, dict):
                            if "codes" in result:
                                codes.extend(code["code"] for code in result["codes"] if isinstance(code, dict) and "code" in code)
                            if "explanation" in result:
                                explanation.append(result["explanation"])
                    
                    parsed_data = {
                        "specific_codes": codes,
                        "explanation": " ".join(explanation) if explanation else "Codes extracted from diagnostic services",
                        "doubt": "None"
                    }
                    
                    self.update_values(
                        name=self.name or "Dental Code Analysis",
                        strict=True,
                        explanation=parsed_data["explanation"],
                        doubt=parsed_data["doubt"],
                        code_range=self.schema["code_range"],
                        activated_subtopics=self.schema["activated_subtopics"],
                        specific_codes=parsed_data["specific_codes"]
                    )
                    return [parsed_data]  # Return as a list for consistency

            except (json.JSONDecodeError, AttributeError):
                pass

            # Regex-based parsing for raw_output
            sections = re.split(r'(?=EXPLANATION:)', raw_output.strip())
            parsed_data_list = []

            for section in sections:
                if not section.strip():
                    continue
                
                # Extract code
                code_match = re.search(r'CODE:\s*(D\d{4}|none)', section, re.IGNORECASE)
                code = [code_match.group(1)] if code_match and code_match.group(1) != 'none' else []
                
                # Extract explanation
                explanation_match = re.search(r'EXPLANATION:\s*(.*?)(?=\s*DOUBT:|\s*CODE:|$)', section, re.DOTALL | re.IGNORECASE)
                explanation = explanation_match.group(1).strip().replace('\n', ' ') if explanation_match else "No explanation provided"
                
                # Extract doubt
                doubt_match = re.search(r'DOUBT:\s*(.*?)(?=\s*CODE:|$)', section, re.DOTALL | re.IGNORECASE)
                doubt = doubt_match.group(1).strip().replace('\n', ' ') if doubt_match else "None"
                
                # Include all sections, even those with no codes
                parsed_data = {
                    "specific_codes": code,
                    "explanation": explanation,
                    "doubt": doubt
                }
                parsed_data_list.append(parsed_data)

            if not parsed_data_list:
                parsed_data_list.append({
                    "specific_codes": [],
                    "explanation": "No codes or explanation found in the provided raw output",
                    "doubt": "None"
                })

            # Update DentalCodeManager with the first parsed data
            if parsed_data_list:
                self.update_values(
                    name=self.name or "Dental Code Analysis",
                    strict=True,
                    explanation=parsed_data_list[0]["explanation"],
                    doubt=parsed_data_list[0]["doubt"],
                    code_range=self.schema["code_range"],
                    activated_subtopics=self.schema["activated_subtopics"],
                    specific_codes=parsed_data_list[0]["specific_codes"]
                )

            return parsed_data_list

        except Exception as e:
            error_data = {
                "specific_codes": [],
                "explanation": f"Error parsing output: {str(e)}",
                "doubt": "Error occurred during parsing"
            }
            self.update_values(
                name=self.name or "Dental Code Analysis",
                strict=False,
                explanation=error_data["explanation"],
                doubt=error_data["doubt"],
                code_range=self.schema["code_range"],
                activated_subtopics=self.schema["activated_subtopics"],
                specific_codes=[]
            )
            return [error_data]

    def transform_json_list(self, input_json_list: list) -> list:
        """
        Transform a list of topic JSONs by replacing each subtopic's raw_result with a list of parsed JSON objects.
        """
        output_json_list = copy.deepcopy(input_json_list)
        
        for topic_json in output_json_list:
            subtopics_data = topic_json['raw_result']['subtopics_data']
            for subtopic in subtopics_data:
                raw_result = subtopic['raw_result']
                print(f"##########*********Raw Result*******######### : {raw_result}")
                parsed_results = self.parse_llm_output(raw_result)
                subtopic['raw_result'] = parsed_results
        
        return output_json_list

# Example usage with multiple topics
input_json_list = [
    {
        'topic': 'Diagnostic',
        'code_range': 'D0100-D0999',
        'raw_result': {
            'raw_topic_data': "EXPLANATION: The patient presented with specific symptoms (pain, sensitivity) localized to a quadrant, prompting an examination. The objective findings (caries, tenderness) confirm a clinical assessment took place, triggering the **Clinical Oral Evaluations (D0120-D0180)** range (likely a D0140 - Limited evaluation, problem focused). Diagnosing the extent of a large carious lesion and associated symptoms like sensitivity and tenderness necessitates radiographic assessment, making **Diagnostic Imaging (D0210-D0391)** applicable (e.g., periapical or bitewing radiographs). Furthermore, the symptoms (sensitivity to hot/cold, tenderness) strongly indicate the need for pulp vitality assessment to determine the tooth's pulpal status, thus involving the **Tests and Laboratory Examinations (D0411-D0999)** range (specifically D0460 - pulp vitality tests).\nDOUBT: The scenario does not explicitly state that diagnostic imaging or pulp vitality tests were performed during this specific visit, only that the clinical findings and assessment were made. However, these diagnostic procedures are standard practice and essential for reaching the assessment described, making their corresponding code ranges applicable for a complete diagnostic workup of this nature. If these procedures were not performed, they would not be billed, but the ranges are relevant to the clinical situation presented.\nCODE RANGE: D0120-D0180, D0210-D0391, D0411-D0999",
            'code_range': 'D0100-D0999',
            'activated_subtopics': [
                'Clinical Oral Evaluations (D0120-D0180)',
                'Diagnostic Imaging (D0210-D0391)',
                'Tests and Laboratory Examinations (D0411-D0999)'
            ],
            'subtopics_data': [
                {
                    'topic': 'Clinical Oral Evaluations (D0120-D0180)',
                    'code_range': 'D0120-D0180',
                    'raw_result': 'EXPLANATION: The patient presented with a specific problem (pain, sensitivity in the lower right quadrant) related to a specific tooth (#27 with a large carious lesion). This visit was focused solely on evaluating this acute issue, which aligns directly with the definition of a limited, problem-focused evaluation.\nDOUBT: None\nCODE: D0140',
                    'error': None
                },
                {
                    'topic': 'Diagnostic Imaging (D0210-D0391)',
                    'code_range': 'D0210-D0391',
                    'raw_result': "EXPLANATION: The scenario describes a patient presenting with localized pain and clinical findings suggestive of pathology on tooth #27. Guideline 1 suggests D0220 (first periapical) is appropriate for localized pain/pathology. This code would be used for the initial image taken to assess the specific tooth (#27) and its periapical area due to the reported symptoms and clinical findings. However, the scenario describes only the patient's complaints and the dentist's clinical findings/assessment; it does *not* explicitly state that any radiographs were actually taken during this visit. Coding requires that the procedure was performed. Assuming an image *was* taken based on the clinical need: D0220 would be the code for the first periapical image.\nDOUBT: The scenario does not explicitly state that any radiographs were taken during this visit. The coding assumes that the standard of care for evaluating these symptoms would include at least one periapical radiograph and that it was performed, even though not explicitly documented in the provided text.\nCODE: D0220\n\nEXPLANATION: Guideline 1 suggests D0230 (additional periapical) may be used in conjunction with D0220 for localized pain/pathology. Tooth #27 is a molar, which often requires more than one periapical image to adequately visualize all roots and surrounding structures, especially when assessing pain and extensive caries. Therefore, an additional periapical image might have been taken. However, similar to D0220, the scenario does not explicitly state that *any* radiographs, let alone *additional* ones, were taken. Coding requires the procedure was performed. Assuming a second image *was* taken based on clinical need for a molar evaluation: D0230 would be the code for the second periapical image.\nDOUBT: The scenario does not explicitly state that any radiographs were taken, nor does it specify if more than one periapical image was captured if one was indeed taken. This coding assumes a second PA was taken based on common practice for molar evaluation, but this is an assumption not directly supported by the text.\nCODE: D0230",
                    'error': None
                },
                {
                    'topic': 'Tests and Laboratory Examinations (D0411-D0999)',
                    'code_range': 'D0411-D0999',
                    'raw_result': "EXPLANATION: The patient presents with symptoms (pain, sensitivity, tenderness to percussion) and clinical findings (large carious lesion) suggestive of pulpal involvement in tooth #27. A pulp vitality test (D0460) would be a logical diagnostic procedure to assess the health of the pulp before determining treatment. This test helps differentiate between reversible pulpitis, irreversible pulpitis, or necrosis.\nDOUBT: The scenario describes the patient's symptoms and the dentist's objective findings and assessment, strongly indicating the need for pulp testing. However, it does not explicitly state that pulp vitality tests *were performed* during this specific visit. Coding should only reflect procedures completed. If the tests were indeed performed, this code is appropriate. If they were planned for a future visit or not done, this code should not be used. Assuming the assessment included performing the necessary diagnostic tests like pulp vitality testing given the symptoms.\nCODE: D0460",
                    'error': None
                }
            ]
        },
        'error': None
    },
    {
        'topic': 'Restorative',
        'code_range': 'D2000-D2999',
        'raw_result': {
            'raw_topic_data': 'EXPLANATION: The scenario describes a patient presenting with symptoms related to a large carious lesion on tooth #27. Although no restorative treatment was performed or explicitly recommended *during this specific visit*, the diagnosis strongly implies the need for future restorative intervention. Based on the finding of a "large carious lesion" with associated symptoms on a molar, several restorative options are potentially indicated. A large lesion might necessitate full coverage (Crowns), potentially requiring auxiliary services like a core buildup (Other Restorative Services). Alternatively, depending on the exact extent and remaining tooth structure, an indirect restoration (Inlay/Onlay) or a large direct restoration (Amalgam or Composite) could be considered. Therefore, these ranges represent the potential restorative treatments that address the diagnosed condition.\nDOUBT: The provided scenario details a diagnostic visit where a large carious lesion was identified, but no restorative treatment was performed or documented as recommended *in this encounter*. Therefore, while the listed code ranges represent potential future treatments indicated by the diagnosis, no codes from these restorative ranges should be billed for the visit described in the scenario itself. Billing for this visit would likely involve evaluation and management codes and potentially diagnostic codes (e.g., radiographs), not restorative codes.\nCODE RANGE: D2710-D2799, D2910-D2999, D2510-D2664, D2140-D2161, D2330-D2394',
            'code_range': 'D2000-D2999',
            'activated_subtopics': [
                'Amalgam Restorations (D2140-D2161)',
                'Crowns (D2710-D2799)',
                'Inlays and Onlays (D2510-D2664)',
                'Other Restorative Services (D2910-D2999)',
                'Resin-Based Composite Restorations (D2330-D2394)'
            ],
            'subtopics_data': [
                {
                    'topic': 'Amalgam Restorations (D2140-D2161)',
                    'code_range': 'D2140-D2161',
                    'raw_result': 'EXPLANATION: The provided scenario describes the patient\'s symptoms, clinical findings (large carious lesion on #27), and assessment. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." The codes D2140, D2150, D2160, and D2161 are for the *placement* of amalgam restorations. Since no amalgam restoration was performed during this visit, none of these specific codes apply.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Resin-Based Composite Restorations (D2330-D2394)',
                    'code_range': 'D2330-D2394',
                    'raw_result': 'EXPLANATION: The scenario describes the patient\'s symptoms, clinical findings (large carious lesion on tooth #27), and assessment. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." The provided codes (D2330-D2394) are for the *placement* of direct resin-based composite restorations. Since no restorative procedure was performed during this visit, none of these codes are applicable. The visit likely consisted of an evaluation and diagnosis, which would be coded using different CDT codes not included in the provided list.\nDOUBT: The scenario incorrectly identifies tooth #27 as a mandibular right first molar; it is the mandibular right canine (an anterior tooth). This discrepancy could affect future coding if a restoration is planned, but it doesn\'t change the fact that no restoration was performed *in this visit*. The description mentions a "large" lesion but doesn\'t specify surfaces, which would be needed if a restoration *had* been done.\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Inlays and Onlays (D2510-D2664)',
                    'code_range': 'D2510-D2664',
                    'raw_result': 'EXPLANATION: The scenario describes an initial patient visit for pain and sensitivity, leading to the diagnosis of a large carious lesion on tooth #27. No restorative treatment (inlay or onlay) was performed during this visit according to the "Treatment Provided" section. The provided codes are exclusively for completed inlay/onlay restorations.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Crowns (D2710-D2799)',
                    'code_range': 'D2710-D2799',
                    'raw_result': 'EXPLANATION: The provided scenario describes an initial patient visit for pain and sensitivity related to a large carious lesion on tooth #27. An assessment was made, but no restorative treatment, specifically the placement of any type of crown (resin, PFM, metal, ceramic, full, 3/4, or interim), was performed during this visit according to the "Treatment Provided" section. The codes listed (D2710-D2799) are all for the placement of single crown restorations. Since no crown was placed, none of these codes are applicable to this encounter.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Other Restorative Services (D2910-D2999)',
                    'code_range': 'D2910-D2999',
                    'raw_result': 'EXPLANATION: The scenario describes a patient presenting with symptoms related to a large carious lesion on tooth #27. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." All codes in the provided list (D2910-D2999) describe specific restorative procedures (e.g., re-cementations, crowns, buildups, repairs, veneers, protective restorations). Since no restorative treatment was performed during this visit, none of these codes apply. The visit likely consisted of an examination and diagnosis, which would be coded differently (e.g., D0140, D0150), but those codes are not available in the provided list.\nDOUBT: The objective notes tooth #27 as a "mandibular right first molar," which is incorrect; #27 is the mandibular right canine. Assuming #27 is the correct tooth number, the description fits a canine. If the intent was the first molar (#30), the assessment remains the same as no treatment was performed.\nCODE: none',
                    'error': None
                }
            ]
        },
        'error': None
    },
    {
        'topic': 'Endodontics',
        'code_range': 'D3000-D3999',
        'raw_result': {
            'raw_topic_data': "EXPLANATION: The patient presents with symptoms (persistent pain, sensitivity, pain on chewing) and clinical findings (large caries, tenderness to percussion) on tooth #27, a permanent molar, strongly suggesting irreversible pulpitis or necrosis. This presentation most directly points towards the need for complete root canal treatment (D3310-D3333). A pulpotomy (D3220-D3222) might be considered as an emergency palliative procedure given the significant pain. The presence of a large carious lesion also activates the pulp capping range (D3110-D3120) as a potential, though less likely, consideration during caries removal if the pulp status allowed. Finally, 'Other Endodontic Procedures' (D3910-D3999) is included as procedures like isolation or canal prep for post might eventually be necessary in conjunction with or following definitive endodontic treatment.\nDOUBT: The scenario describes the initial presentation and assessment but does not specify any treatment performed or definitively recommended during this visit. Therefore, these code ranges represent the *potential* treatments indicated by the diagnosis, rather than procedures already completed or confirmed in a treatment plan. The final choice of treatment would depend on further diagnostic tests (e.g., pulp vitality testing, radiographs) and clinical decisions.\nCODE RANGE: D3310-D3333, D3220-D3222, D3110-D3120, D3910-D3999",
            'code_range': 'D3000-D3999',
            'activated_subtopics': [
                'Endodontic Therapy (D3310-D3333)',
                'Other Endodontic Procedures (D3910-D3999)',
                'Pulp Capping (D3110-D3120)',
                'Pulpotomy (D3220-D3222)'
            ],
            'subtopics_data': [
                {
                    'topic': 'Pulp Capping (D3110-D3120)',
                    'code_range': 'D3110-D3120',
                    'raw_result': 'EXPLANATION: The scenario describes the patient\'s initial presentation with symptoms and clinical findings related to a large carious lesion on tooth #27. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." Both D3110 (Direct Pulp Cap) and D3120 (Indirect Pulp Cap) are codes for specific treatment procedures involving the application of a protective dressing to the pulp or near-pulp area. Since no such treatment was performed during this visit, neither code is applicable.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Pulpotomy (D3220-D3222)',
                    'code_range': 'D3220-D3222',
                    'raw_result': "EXPLANATION: The scenario describes the patient's symptoms, clinical findings (large caries on #27, tenderness), and assessment, but explicitly states that no treatment was provided during this visit. Codes D3220, D3221, and D3222 represent specific procedures (therapeutic pulpotomy, pulpal debridement, partial pulpotomy for apexogenesis) involving removal of pulp tissue. Since no such procedure was performed, none of these codes are applicable to this encounter.\nDOUBT: None\nCODE: none",
                    'error': None
                },
                {
                    'topic': 'Endodontic Therapy (D3310-D3333)',
                    'code_range': 'D3310-D3333',
                    'raw_result': 'EXPLANATION: The patient presented with symptoms (pain, sensitivity, tenderness to percussion) and clinical findings (large carious lesion) on tooth #27, a molar, strongly suggesting the need for endodontic therapy. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." The provided codes (D3310-D3333) are for specific endodontic *procedures* (therapy, obstruction treatment, incomplete therapy, perforation repair). Since no endodontic procedure was performed during this visit, none of these codes apply. This visit likely involved evaluation and diagnosis, which would use different codes not included in the provided list.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Other Endodontic Procedures (D3910-D3999)',
                    'code_range': 'D3910-D3999',
                    'raw_result': 'EXPLANATION: The scenario describes a patient presenting with symptoms (pain, sensitivity) related to a large carious lesion on tooth #27. This visit appears to be diagnostic in nature, involving subjective complaints, objective findings (caries, tenderness), and an assessment. No specific endodontic procedure from the provided list (D3910, D3911, D3920, D3921, D3950, D3999) was performed during this encounter. These codes represent specific treatments like surgical isolation, barrier placement, hemisection, decoronation, post preparation, or unspecified procedures, none of which occurred.\nDOUBT: None\nCODE: none',
                    'error': None
                }
            ]
        },
        'error': None
    },
    {
        'topic': 'Oral and Maxillofacial Surgery',
        'code_range': 'D7000-D7999',
        'raw_result': {
            'raw_topic_data': "EXPLANATION: The provided scenario describes a patient presenting with symptoms related to a large carious lesion on tooth #27. The visit details subjective complaints, objective findings, and an assessment. Crucially, no treatment was provided during this visit, and no specific surgical procedures were recommended or planned within this encounter's documentation. All the listed code ranges pertain to surgical interventions (extractions, lesion removals, bone modifications, fracture repairs, etc.). Since no surgical procedure was performed or documented as planned for this specific visit, none of the Oral and Maxillofacial Surgery code ranges (D7000 series) are applicable for billing this particular encounter. The visit itself would likely be coded under Evaluation and Management (e.g., D0140, D0150) and potentially diagnostic codes (e.g., radiographs), but not surgical codes.\nDOUBT: The scenario only describes the diagnostic phase. Future treatment for the large carious lesion on tooth #27 might involve procedures falling into the D7111-D7140 (Simple Extractions) or D7210-D7251 (Surgical Extractions) ranges, depending on the tooth's condition and the complexity of removal. However, based *solely* on the information provided for *this visit*, no surgical codes apply.\nCODE RANGE: none",
            'code_range': 'D7000-D7999',
            'activated_subtopics': [],
            'subtopics_data': []
        },
        'error': None
    },
    {
        'topic': 'Adjunctive General Services',
        'code_range': 'D9000-D9999',
        'raw_result': {
            'raw_topic_data': 'EXPLANATION: The patient presented with acute symptoms (persistent pain, sensitivity, pain on chewing) indicative of an emergency situation requiring immediate attention. This directly triggers the D9110-D9130 range for palliative/emergency management of dental pain and sensitivity, even if definitive treatment was deferred. The sensitivity complaint also weakly triggers the D9910-D9973 range, as desensitization (D9910) is a potential component of managing such symptoms, although no specific application was documented in this note.\nDOUBT: The primary uncertainty arises from the "Treatment Provided: None mentioned" statement. While D9110 represents palliative *treatment*, it\'s often used to code the management of an emergency pain visit itself. Similarly, D9910 requires *application* of medicament, which wasn\'t explicitly stated. However, given the strong subjective complaints defining the visit\'s purpose (emergency pain/sensitivity relief), these ranges are the most applicable within the D9xxx series based on the activation triggers. The actual billing would depend on whether any minimal palliative action or desensitizing application occurred, even if poorly documented, or if the office policy uses D9110 for managing the emergency visit itself alongside an evaluation code.\nCODE RANGE: D9110-D9130, D9910-D9973',
            'code_range': 'D9000-D9999',
            'activated_subtopics': [
                'Miscellaneous Services (D9910-D9973)',
                'Unclassified Treatment (D9110-D9130)'
            ],
            'subtopics_data': [
                {
                    'topic': 'Unclassified Treatment (D9110-D9130)',
                    'code_range': 'D9110-D9130',
                    'raw_result': 'EXPLANATION: The scenario describes a patient visit for evaluation of pain, leading to the identification of a large carious lesion on tooth #27. However, the "Treatment Provided" section explicitly states "None mentioned in this visit description." The code D9999 is for an *unspecified adjunctive procedure* that was actually *performed*. Since no procedure, specified or unspecified, was performed during this visit according to the notes, D9999 is not applicable. The visit likely consisted of an evaluation/examination, which would be coded differently (e.g., D0140, D0150), but those codes are not available in the provided list.\nDOUBT: None\nCODE: none',
                    'error': None
                },
                {
                    'topic': 'Miscellaneous Services (D9910-D9973)',
                    'code_range': 'D9910-D9973',
                    'raw_result': 'EXPLANATION: The patient presented for evaluation of pain related to a large carious lesion on tooth #27. No treatment from the provided list (desensitization, behavior management, post-surgical care, denture/appliance services, occlusal analysis/adjustment, cosmetic procedures) was performed during this visit. The visit focused on diagnosis, which is not covered by the miscellaneous codes provided.\nDOUBT: None\nCODE: none',
                    'error': None
                }
            ]
        },
        'error': None
    }
]

# Initialize DentalCodeManager
dental_manager = DentalCodeManager()

# Transform the JSON list
output_json_list = dental_manager.transform_json_list(input_json_list)

# Print the transformed JSON
print(json.dumps(output_json_list, indent=4))