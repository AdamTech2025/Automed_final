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

class AnesthesiaServices:
    """Class to analyze and extract anesthesia codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing anesthesia services."""
        return PromptTemplate(
            template=f"""
You are a medical coding expert,

## **Anesthesia**

### **Before picking a code, ask:**
- What level of anesthesia is required—local, regional, moderate sedation, deep sedation, or general anesthesia?
- Is the anesthesia being used for an operative/surgical procedure, or is it a standalone service?
- What method is being used—local injection, inhalation, IV, or another route?
- How long is the anesthesia being administered?
- Does the patient have any medical conditions that may require special monitoring or modification of anesthesia type?
- What is the goal of anesthesia—pain relief, anxiety reduction, or complete unconsciousness?

---

#### **Code: D9210** – *Local anesthesia not in conjunction with operative or surgical procedures*
**Use when:** Providing local anesthetic injections for pain relief without performing a surgical or operative procedure.
**Check:** Ensure the anesthesia is used for diagnostic or pain-relief purposes and is not part of another billed procedure.
**Note:** This is a standalone procedure, typically used for acute pain management, such as during a dental emergency or prior to a minor diagnostic procedure.

#### **Code: D9211** – *Regional block anesthesia*
**Use when:** Anesthetizing a broader region by injecting anesthesia near a major nerve or nerve cluster.
**Check:** Verify that a regional nerve block is necessary for extensive procedures rather than standard local infiltration.
**Note:** Commonly used for mandibular molar extractions, complex restorations, or periodontal surgeries requiring prolonged numbing.

#### **Code: D9212** – *Trigeminal division block anesthesia*
**Use when:** Providing anesthesia by blocking one of the three main branches of the trigeminal nerve (ophthalmic, maxillary, or mandibular).
**Check:** Confirm documentation specifies which division is blocked and why a more extensive nerve block is required.
**Note:** Used for complex surgical extractions, severe trauma cases, or extensive restorative procedures requiring prolonged numbing in a large facial region.

#### **Code: D9215** – *Local anesthesia in conjunction with operative or surgical procedures*
**Use when:** Providing local anesthesia as part of another procedure, such as an extraction, filling, or periodontal surgery.
**Check:** Ensure that this is not billed separately when anesthesia is included in the main procedure code.
**Note:** This code is not billed independently—it is recorded as part of the primary dental service.

#### **Code: D9219** – *Evaluation for moderate sedation, deep sedation, or general anesthesia*
**Use when:** Conducting a pre-anesthesia assessment to evaluate a patient's suitability for sedation.
**Check:** Ensure that the assessment includes documentation of medical history, risk factors, and anesthesia planning.
**Note:** This code is used for comprehensive anesthesia evaluations but not for routine local anesthetic administration.

---

### **Deep Sedation and General Anesthesia**

#### **Code: D9222** – *Deep sedation/general anesthesia – first 15 minutes*
**Use when:** The patient is placed into a controlled state of unconsciousness where they cannot respond to stimuli.
**Check:** Ensure proper documentation of start time, anesthesia depth, and patient monitoring.
**Note:** This code is time-based; use D9223 for additional increments beyond the first 15 minutes.

#### **Code: D9223** – *Deep sedation/general anesthesia – each subsequent 15-minute increment*
**Use when:** The procedure requires prolonged deep sedation or general anesthesia beyond the initial 15 minutes.
**Check:** Document total sedation time and ensure continuous monitoring.
**Note:** Always use in conjunction with D9222 for accurate billing.

---

### **Nitrous Oxide and Moderate Sedation**

#### **Code: D9230** – *Inhalation of nitrous oxide/analgesia, anxiolysis*
**Use when:** Administering nitrous oxide to reduce anxiety and provide mild sedation.
**Check:** Ensure the patient's medical history allows nitrous oxide use and document the total duration.
**Note:** Common for pediatric patients, anxious adults, or minor dental procedures requiring mild relaxation.

#### **Code: D9239** – *Intravenous moderate (conscious) sedation/analgesia – first 15 minutes*
**Use when:** Administering IV sedation to create a state of deep relaxation while keeping the patient conscious.
**Check:** Document the start and stop time, patient's response, and monitoring throughout the procedure.
**Note:** Used for procedures like wisdom tooth extractions, implant placement, or complex oral surgeries.

#### **Code: D9243** – *Intravenous moderate (conscious) sedation/analgesia – each subsequent 15-minute increment*
**Use when:** The procedure requires continued IV moderate sedation beyond the first 15 minutes.
**Check:** Ensure the total duration of IV sedation is accurately documented.
**Note:** Always billed alongside D9239 for extended sedation periods.

#### **Code: D9248** – *Non-intravenous conscious sedation*
**Use when:** Administering sedation through non-IV routes (e.g., oral tablets, intramuscular injections).
**Check:** Ensure that the sedation level allows the patient to maintain their airway and respond to stimuli.
**Note:** Common for mild to moderate sedation in patients with dental anxiety or those undergoing minor surgical procedures.

---

### **Key Takeaways:**
- **Local anesthesia (D9210, D9215)** is used for pain control and is either billed separately (D9210) or included in another procedure (D9215).
- **Regional and nerve block anesthesia (D9211, D9212)** provide deeper numbing for more complex cases.
- **Deep sedation/general anesthesia (D9222, D9223)** is used for unconscious sedation and is time-based.
- **Nitrous oxide (D9230)** is used for mild sedation, mainly for anxious patients or short procedures.
- **IV moderate sedation (D9239, D9243)** and **non-IV sedation (D9248)** are commonly used for procedures requiring deeper relaxation while maintaining consciousness.
- **Accurate documentation** of anesthesia type, duration, and patient response is critical for correct billing and patient safety.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_anesthesia_code(self, scenario: str) -> str:
        """Extract anesthesia code(s) for a given scenario."""
        try:
            print(f"Analyzing anesthesia scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Anesthesia extract_anesthesia_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in anesthesia code extraction: {str(e)}")
            return ""
    
    def activate_anesthesia(self, scenario: str) -> str:
        """Activate the anesthesia analysis process and return results."""
        try:
            result = self.extract_anesthesia_code(scenario)
            if not result:
                print("No anesthesia code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating anesthesia analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_anesthesia(scenario)
        print(f"\n=== ANESTHESIA ANALYSIS RESULT ===")
        print(f"ANESTHESIA CODE: {result if result else 'None'}")



anesthesia_service = AnesthesiaServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an anesthesia dental scenario: ")
    anesthesia_service.run_analysis(scenario)