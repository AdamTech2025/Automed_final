import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature


# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Import modules
from subtopics.prompt.prompt import PROMPT

class NonClinicalProceduresServices:
    """Class to analyze and extract non-clinical procedure codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing non-clinical procedures."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert

Before picking a code, ask:
- What is the nature of the service being documented—administrative, patient support, or a missed obligation?
- Does the service require additional time, resources, or documentation to justify its use?
- Is the code tied to a specific patient interaction, or does it reflect a broader case management effort?
Accurate coding for non-clinical procedures ensures proper billing, compliance, and documentation of services that enhance patient care or practice operations.

---

#### Code: D9961 - Duplicate/Copy Patient's Records
**When to use:**
This code is used when a patient or authorized entity requests a duplicate or copy of their dental records.
**What to check:**
- Verify the requestor's identity and authorization to receive the records.
- Ensure the duplicated records include all relevant documentation (charts, X-rays, notes).
**Notes:**
- This is an administrative service, not tied to clinical care; chargeable as a separate fee if applicable.
- Maintain a log of when and to whom records are provided for compliance.

---

#### Code: D9985 - Sales Tax
**When to use:**
Apply this code to document sales tax charged on dental services or products, where applicable by local law.
**What to check:**
- Confirm if sales tax applies to the specific service or item per jurisdictional regulations.
- Calculate the correct tax amount based on the taxable portion of the bill.
**Notes:**
- This is a pass-through cost, not a dental service; ensure transparency in billing.
- Not all states or regions require sales tax on dental procedures—verify local rules.

---

#### Code: D9986 - Missed Appointment
**When to use:**
Use this code when a patient fails to attend a scheduled appointment without prior notice.
**What to check:**
- Confirm the appointment was scheduled and the patient was notified of the date and time.
- Review practice policy on charging for missed appointments.
**Notes:**
- This is a non-clinical fee to compensate for lost time; not reimbursable by insurance.
- Clearly communicate the missed appointment policy to patients in advance.

---

#### Code: D9987 - Cancelled Appointment
**When to use:**
This code applies when a patient cancels an appointment, typically within a timeframe specified by practice policy (e.g., less than 24 hours' notice).
**What to check:**
- Verify the cancellation timing against the practice's cancellation policy.
- Document the reason for cancellation, if provided, for internal records.
**Notes:**
- Differs from D9986 as it involves active cancellation rather than a no-show.
- May or may not incur a fee, depending on practice guidelines.

---

#### Code: D9990 - Certified Translation or Sign-Language Services - Per Visit
**When to use:**
Use when providing certified translation or sign-language services to facilitate communication during a patient visit.
**What to check:**
- Ensure the service is performed by a certified professional during the appointment.
- Document the need for the service (e.g., language barrier, hearing impairment).
**Notes:**
- This enhances accessibility; may be billable depending on practice or insurance policies.
- Applies per visit, not per hour or minute of service.

---

#### Code: D9991 - Dental Case Management - Addressing Appointment Compliance Barriers
**When to use:**
This code is for individualized efforts to help a patient overcome barriers (e.g., transportation) to keep scheduled appointments.
**What to check:**
- Identify and document the specific barrier (e.g., lack of transport, scheduling conflicts).
- Record the actions taken to assist (e.g., arranging rides, rescheduling).
**Notes:**
- Focuses on practical solutions to improve compliance, not clinical care.
- Requires documentation of efforts for justification.

---

#### Code: D9992 - Dental Case Management - Care Coordination
**When to use:**
Use when coordinating oral health care across multiple providers, specialties, or systems, requiring extra time and expertise.
**What to check:**
- Confirm involvement of multiple providers or settings (e.g., dentist, specialist, hospital).
- Document the coordination efforts and their purpose (e.g., treatment planning, referrals).
**Notes:**
- Reflects additional administrative effort beyond patient's own capacity.
- Not for routine scheduling—focus is on complex cases.

---

#### Code: D9993 - Dental Case Management - Motivational Interviewing
**When to use:**
Apply this code for patient-centered counseling (e.g., Motivational Interviewing) to address behaviors affecting oral health.
**What to check:**
- Verify the use of structured techniques like MI to modify behavior (e.g., smoking cessation, hygiene habits).
- Document the session's goals and outcomes.
**Notes:**
- Separate from nutritional or tobacco counseling; focuses on personalized behavior change.
- Requires training in motivational techniques for proper application.

---

#### Code: D9994 - Dental Case Management - Patient Education to Improve Oral Health Literacy
**When to use:**
This code is for customized education to enhance a patient's oral health literacy, tailored to their cultural and economic context.
**What to check:**
- Assess the patient's current understanding and barriers to oral health knowledge.
- Document the tailored education provided and its delivery method.
**Notes:**
- Goes beyond standard case presentation; requires extra time and adaptation.
- Aims to empower patients for better health decisions.

---

#### Code: D9997 - Dental Case Management - Patients with Special Health Care Needs
**When to use:**
Use for patients with physical, medical, developmental, or cognitive conditions requiring modified treatment delivery.
**What to check:**
- Identify the specific condition (e.g., autism, wheelchair-bound) and its impact on care.
- Document modifications made (e.g., extended time, sedation, special equipment).
**Notes:**
- Focuses on accommodations for comprehensive care, not just routine adjustments.
- May overlap with clinical codes but emphasizes management effort.

---

#### Code: D9995 - Teledentistry - Synchronous; Real-Time Encounter
**When to use:**
This code is reported alongside other procedures for real-time virtual consultations on the date of service.
**What to check:**
- Ensure the encounter occurs live via audio/video with the patient.
- Document the procedure(s) performed remotely (e.g., diagnostic review).
**Notes:**
- Additive code—pair with clinical codes like D0140 or D0150.
- Requires technology enabling immediate interaction.

---

#### Code: D9996 - Teledentistry - Asynchronous; Information Stored and Forwarded to Dentist for Subsequent Review
**When to use:**
Use with other procedures when patient data (e.g., images, records) is collected and sent for later dentist review.
**What to check:**
- Verify data is stored and forwarded (e.g., photos, X-rays) rather than reviewed in real time.
- Link to the associated clinical procedure code.
**Notes:**
- Additive code for non-live interactions; contrasts with D9995.
- Useful for follow-ups or consultations not requiring immediate response.

---

#### Code: D9999 - Unspecified Adjunctive Procedure, by Report
**When to use:**
Apply this code for a non-clinical procedure not covered by existing codes, requiring a detailed explanation.
**What to check:**
- Confirm no other specific code applies to the service.
- Provide a narrative report describing the procedure, purpose, and resources used.
**Notes:**
- Broad catch-all code; specificity in documentation is critical for approval or billing.
- Avoid overuse—search for a more precise code first.

---

### Key Takeaways:
- Non-clinical codes capture administrative, supportive, or patient management services, not direct treatment.
- Documentation is essential, especially for case management (D9991-D9997) and unspecified procedures (D9999).
- Teledentistry codes (D9995, D9996) enhance flexibility but must pair with clinical codes.
- Fees for missed/cancelled appointments (D9986, D9987) depend on practice policy and patient communication.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_non_clinical_procedures_code(self, scenario: str) -> str:
        """Extract non-clinical procedure code(s) for a given scenario."""
        try:
            print(f"Analyzing non-clinical procedures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Non-clinical procedures extract_non_clinical_procedures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in non-clinical procedures code extraction: {str(e)}")
            return ""
    
    def activate_non_clinical_procedures(self, scenario: str) -> str:
        """Activate the non-clinical procedures analysis process and return results."""
        try:
            result = self.extract_non_clinical_procedures_code(scenario)
            if not result:
                print("No non-clinical procedures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating non-clinical procedures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_non_clinical_procedures(scenario)
        print(f"\n=== NON-CLINICAL PROCEDURES ANALYSIS RESULT ===")
        print(f"NON-CLINICAL PROCEDURES CODE: {result if result else 'None'}")

non_clinical_service = NonClinicalProceduresServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a non-clinical procedures dental scenario: ")
    non_clinical_service.run_analysis(scenario)