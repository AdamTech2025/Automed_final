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

class MiscellaneousServices:
    """Class to analyze and extract miscellaneous service codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing miscellaneous services."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert

## **Miscellaneous Dental Services**

### **Before selecting a code, ask:**
- Is the treatment related to desensitization, behavioral management, or post-surgical complications?
- Is the procedure related to denture or occlusal appliance cleaning, adjustment, or fabrication?
- Is the service addressing sleep apnea, occlusal analysis, or tooth reshaping?
- Is the procedure focused on cosmetic enhancements such as bleaching or enamel modification?

**Code: D9910 – Application of Desensitizing Medicament**
**Use when:** A dentist applies a topical desensitizing agent to relieve root sensitivity. Commonly used for patients experiencing discomfort from exposed dentin.
**Check:** Ensure the application is performed in-office and not prescribed for home use.
**Note:** This does not include liners, bases, or adhesives used under restorations.

**Code: D9911 – Application of Desensitizing Resin for Cervical and/or Root Surface, Per Tooth**
**Use when:** A dentist applies adhesive resins to desensitize and protect root surfaces from further irritation. This is especially beneficial for patients with receding gums.
**Check:** Verify that the application is done per tooth and not as a generalized treatment.
**Note:** Not to be confused with bases or liners used under restorations.

**Code: D9912 – Pre-Visit Patient Screening**
**Use when:** A dental office conducts health screenings before the scheduled treatment to evaluate the risk of infectious disease transmission.
**Check:** Ensure documentation includes symptoms, recent travel history, and other relevant health factors.
**Note:** Typically used during pandemics or for immunocompromised patients.

**Code: D9920 – Behavior Management, By Report**
**Use when:** Additional time, effort, or resources are required to manage a patient's behavior during dental treatment, such as for children or special needs patients.
**Check:** Report in 15-minute increments and provide documentation of the management techniques used.
**Note:** This is billed in addition to the primary treatment procedure.

**Code: D9930 – Treatment of Complications (Post-Surgical) - Unusual Circumstances, By Report**
**Use when:** A patient requires treatment for complications following oral surgery, such as dry sockets or removal of bone fragments.
**Check:** Ensure detailed documentation of the complication and the additional treatment provided.
**Note:** This code applies only to post-surgical issues, not routine follow-ups.

**Code: D9932 – Cleaning and Inspection of Removable Complete Denture, Maxillary**
**Use when:** A dentist or hygienist cleans and inspects a patient's maxillary (upper) complete denture to maintain hygiene and function.
**Check:** Ensure the patient has a fully removable complete denture, not a partial denture or fixed prosthetic.
**Note:** This service does not include adjustments or relining.

**Code: D9933 – Cleaning and Inspection of Removable Complete Denture, Mandibular**
**Use when:** A dentist or hygienist cleans and inspects a patient's mandibular (lower) complete denture for deposits, cracks, or damage.
**Check:** Confirm that the denture is removable and does not require adjustments or relining.
**Note:** Should be performed periodically to prevent infections and ensure proper function.

**Code: D9934 – Cleaning and Inspection of Removable Partial Denture, Maxillary**
**Use when:** The upper partial denture is professionally cleaned and inspected for wear, fractures, or buildup of plaque and calculus.
**Check:** Ensure the patient has a removable maxillary partial denture, not a full denture or implant-supported prosthesis.
**Note:** Adjustments or relining should be coded separately.

**Code: D9935 – Cleaning and Inspection of Removable Partial Denture, Mandibular**
**Use when:** The lower partial denture undergoes professional cleaning and examination to maintain its function and longevity.
**Check:** Verify that the denture is a removable mandibular partial denture and does not require adjustments.
**Note:** Regular cleanings help prevent irritation and infections in the oral tissues.

**Code: D9941 – Fabrication of Athletic Mouthguard**
**Use when:** A custom-fitted mouthguard is created for a patient involved in sports or activities with high impact risks.
**Check:** Ensure the mouthguard is fabricated specifically for athletic use, not for nighttime bruxism.
**Note:** Different from an occlusal guard, which is used for managing grinding and clenching.

**Code: D9942 – Repair and/or Reline of Occlusal Guard**
**Use when:** An occlusal guard (nightguard) is repaired or relined due to wear, damage, or improper fit.
**Check:** Ensure the guard was previously fabricated and used by the patient before repair.
**Note:** Relining can involve either soft or hard materials depending on the patient's needs.

**Code: D9943 – Occlusal Guard Adjustment**
**Use when:** A previously made occlusal guard requires minor adjustments to improve fit and comfort.
**Check:** Ensure that the adjustment is necessary due to discomfort, occlusal changes, or minor wear.
**Note:** Does not include major repairs or fabrication of a new guard.

**Code: D9944 – Occlusal Guard - Hard Appliance, Full Arch**
**Use when:** A custom-made hard occlusal guard is provided for full arch protection against bruxism and clenching.
**Check:** Ensure that the guard covers the full arch and is made of hard acrylic or similar material.
**Note:** Not used for treating sleep apnea or TMD appliances.

**Code: D9945 – Occlusal Guard - Soft Appliance, Full Arch**
**Use when:** A soft material occlusal guard is made to protect teeth from mild bruxism or other occlusal issues.
**Check:** Ensure the appliance is a soft version and covers the full arch for protection.
**Note:** Typically used for patients with mild grinding issues.

**Code: D9946 – Occlusal Guard - Hard Appliance, Partial Arch**
**Use when:** A hard occlusal appliance is provided but covers only part of the dental arch rather than the full set of teeth.
**Check:** Ensure partial arch coverage and the patient's diagnosis justifies its use.
**Note:** Sometimes used as an anterior deprogrammer for occlusal therapy.

**Code: D9947 – Custom Sleep Apnea Appliance Fabrication and Placement**
**Use when:** A dentist creates and fits a custom oral appliance for sleep apnea management.
**Check:** Ensure the appliance is medically necessary and is distinct from an occlusal guard or snoring device.
**Note:** Often used in collaboration with a sleep physician.

**Code: D9948 – Adjustment of Custom Sleep Apnea Appliance**
**Use when:** A previously delivered sleep apnea appliance needs modification for comfort or function.
**Check:** Confirm that the appliance was custom-made and prescribed for sleep apnea treatment.
**Note:** Minor refinements in fit or repositioning may be required over time.

**Code: D9949 – Repair of Custom Sleep Apnea Appliance**
**Use when:** A sleep apnea appliance is damaged and needs structural repairs rather than a complete replacement.
**Check:** Ensure repairs restore full function without needing a new appliance.
**Note:** Different from relining, which involves resurfacing the inside of the appliance.

**Code: D9950 – Occlusion Analysis - Mounted Case**
**Use when:** A dentist performs a detailed occlusion analysis using diagnostic models mounted on an articulator.
**Check:** Ensure facebow, interocclusal records, and related occlusal studies are documented.
**Note:** Used in comprehensive treatment planning for occlusal or prosthetic rehabilitation.

**Code: D9951 – Occlusal Adjustment - Limited**
**Use when:** Minor reshaping of teeth is performed to correct minor occlusal discrepancies.
**Check:** Ensure that adjustments are limited and not part of routine post-delivery care.
**Note:** Typically used in cases of slight malocclusion or bite discomfort.

**Code: D9952 – Occlusal Adjustment - Complete**
**Use when:** A full occlusal adjustment is performed over multiple appointments to correct disharmonies.
**Check:** Ensure occlusion is analyzed and adjusted systematically to achieve long-term stability.
**Note:** Often used alongside orthodontic, prosthetic, or surgical treatment.

**Code: D9953 – Reline Custom Sleep Apnea Appliance (Indirect)**
**Use when:** A dentist relines the inner surface of a custom sleep apnea appliance to restore its fit and function.
**Check:** Ensure the appliance requires resurfacing with soft or hard material due to wear or changes in the patient's oral structure.
**Note:** This is an indirect procedure, meaning it is performed in a lab rather than chairside.

**Code: D9970 – Enamel Microabrasion**
**Use when:** A minimally invasive procedure is used to remove superficial enamel discoloration caused by mineralization defects, white spots, or mild staining.
**Check:** Confirm that the procedure is done for aesthetic purposes and does not involve deeper layers of enamel.
**Note:** Typically performed per visit and often combined with other cosmetic treatments.

**Code: D9971 – Odontoplasty - Per Tooth**
**Use when:** A dentist reshapes or removes enamel to adjust tooth contours, improve aesthetics, or eliminate minor irregularities.
**Check:** Ensure that only minor modifications are made and that no significant structural changes are involved.
**Note:** Commonly used for cosmetic reshaping, adjusting occlusal interferences, or eliminating sharp edges.

**Code: D9972 – External Bleaching - Per Arch - Performed in Office**
**Use when:** A professional teeth whitening treatment is applied in-office to lighten discoloration and stains on an entire arch of teeth.
**Check:** Verify that the procedure is performed chairside and not as a take-home treatment.
**Note:** Typically involves the use of peroxide-based gels and may include light activation.

**Code: D9973 – External Bleaching - Per Tooth**
**Use when:** A focused whitening treatment is applied to a single tooth, often to correct discoloration that does not match adjacent teeth.
**Check:** Ensure the treatment is performed in-office and not part of a home bleaching kit.
**Note:** Commonly used for individual teeth that have intrinsic staining or post-trauma discoloration.

**Code: D9974 – Internal Bleaching - Per Tooth**
**Use when:** A non-vital tooth (usually after root canal therapy) is whitened from the inside to address discoloration.
**Check:** Confirm that the tooth has undergone endodontic treatment and requires internal whitening due to darkening.
**Note:** The bleaching agent is placed inside the pulp chamber and left for a period before being sealed.

**Code: D9975 – External Bleaching for Home Application, Per Arch**
**Use when:** A custom take-home whitening kit is provided, including trays and professional-grade bleaching gel.
**Check:** Ensure the trays are custom-fitted for the patient and that professional-strength whitening gel is dispensed.
**Note:** This differs from in-office bleaching, as it allows patients to whiten their teeth over several weeks at home.

### **Key Takeaways:**
- **Desensitizing treatments** (D9910-D9911) help manage sensitivity from exposed dentin or cervical lesions.
- **Behavior management (D9920) and post-surgical treatments (D9930)** address special patient care circumstances.
- **Denture cleaning codes (D9932-D9935) apply to maintenance without adjustments.**
- **Mouthguards and occlusal guards (D9941-D9946) focus on bruxism prevention and bite stabilization.**
- **Sleep apnea appliances (D9947-D9953) involve fabrication, repair, and relining of oral devices for airway management.**
- **Occlusal adjustments (D9950-D9952) aim to correct bite imbalances affecting function and comfort.**
- **Cosmetic procedures (D9970-D9975) include microabrasion, odontoplasty, and various teeth whitening options.**

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_miscellaneous_services_code(self, scenario: str) -> str:
        """Extract miscellaneous service code(s) for a given scenario."""
        try:
            print(f"Analyzing miscellaneous services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Miscellaneous services extract_miscellaneous_services_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in miscellaneous services code extraction: {str(e)}")
            return ""
    
    def activate_miscellaneous_services(self, scenario: str) -> str:
        """Activate the miscellaneous services analysis process and return results."""
        try:
            result = self.extract_miscellaneous_services_code(scenario)
            if not result:
                print("No miscellaneous services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating miscellaneous services analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_miscellaneous_services(scenario)
        print(f"\n=== MISCELLANEOUS SERVICES ANALYSIS RESULT ===")
        print(f"MISCELLANEOUS SERVICES CODE: {result if result else 'None'}")


misc_service = MiscellaneousServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a miscellaneous services dental scenario: ")
    misc_service.run_analysis(scenario)