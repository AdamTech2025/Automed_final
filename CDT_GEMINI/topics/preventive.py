import os
import sys
import asyncio
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

from sub_topic_registry import SubtopicRegistry

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Import modules
from topics.prompt import PROMPT

# Import subtopics with fallback mechanism
try:
    from subtopics.Preventive.dental_prophylaxis import dental_prophylaxis_service
    from subtopics.Preventive.topical_fluoride import topical_fluoride_service
    from subtopics.Preventive.other_preventive_services import other_preventive_service
    from subtopics.Preventive.space_maintenance import space_maintenance_service
    from subtopics.Preventive.vaccinations import vaccinations_service
except ImportError:
    print("Warning: Could not import subtopics for Preventive. Using fallback functions.")
    # Define fallback functions if needed
    def activate_dental_prophylaxis(scenario): return None
    def activate_topical_fluoride(scenario): return None
    def activate_other_preventive_services(scenario): return None
    def activate_space_maintenance(scenario): return None
    def activate_vaccinations(scenario): return None

class PreventiveServices:
    """Class to analyze and activate preventive services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D1110-D1120", dental_prophylaxis_service.activate_dental_prophylaxis, 
                            "Dental Prophylaxis (D1110-D1120)")
        self.registry.register("D1206-D1208", topical_fluoride_service.activate_topical_fluoride, 
                            "Topical Fluoride Treatment (D1206-D1208)")
        self.registry.register("D1310-D1355", other_preventive_service.activate_other_preventive_services, 
                            "Other Preventive Services (D1310-D1355)")
        self.registry.register("D1510-D1555", space_maintenance_service.activate_space_maintenance, 
                            "Space Maintenance (D1510-D1555)")
        self.registry.register("D1701-D1707", vaccinations_service.activate_vaccinations, 
                            "Vaccinations (D1701-D1707)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing preventive services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable preventive code range(s) based on the following classifications:

## **Dental Prophylaxis (D1110-D1120)**
**Use when:** Providing routine dental cleaning to remove plaque, calculus, and extrinsic stains from the tooth surfaces and implant abutments to maintain oral health and prevent periodontal disease.
**Check:** Documentation specifies whether the patient is an adult (D1110) with permanent/transitional dentition or a child (D1120) with primary/transitional dentition.
**Note:** Adult prophylaxis (D1110) is typically for patients 14 years and older, while child prophylaxis (D1120) is for patients under 14 years old. These services are distinct from therapeutic periodontal procedures like scaling and root planing.
**Activation trigger:** Scenario mentions OR implies any routine cleaning, dental prophylaxis, removal of plaque/calculus/stains, hygiene appointment, recall visit, regular 6-month checkup with cleaning, maintenance cleaning, or preventive oral hygiene care. INCLUDE this range if there is any indication of professional cleaning or patients coming in for their routine preventive appointment.

## **Topical Fluoride Treatment (D1206-D1208)**
**Use when:** Applying professional fluoride treatments to prevent tooth decay, strengthen enamel, and promote remineralization of early carious lesions.
**Check:** Documentation indicates whether fluoride varnish (D1206) or topical application of fluoride excluding varnish (D1208) was provided, along with the risk assessment supporting the need for fluoride.
**Note:** Fluoride treatments are not limited to children and are indicated for patients with moderate to high caries risk, exposed root surfaces, xerostomia, active orthodontic treatment, or other risk factors for dental caries.
**Activation trigger:** Scenario mentions OR implies any professional fluoride application, fluoride varnish, fluoride gel/foam, fluoride treatment, caries prevention measures, remineralization therapy, or treatment for sensitive teeth with fluoride. INCLUDE this range if there's any hint of professional topical fluoride being applied or considered for caries prevention.

## **Other Preventive Services (D1310-D1355)**
**Use when:** Providing preventive services beyond basic cleaning and fluoride, such as oral hygiene instruction, nutritional counseling, tobacco cessation counseling, sealants, or caries arresting medicaments.
**Check:** Documentation clearly describes the specific preventive service, patient education, counseling provided, or the teeth sealed with preventive resin materials.
**Note:** These codes (D1310-D1355) cover a wide range of preventive interventions designed to reduce risk factors for oral disease, including educational, behavioral, and minimally invasive clinical procedures aimed at preventing future disease rather than treating existing conditions.
**Activation trigger:** Scenario mentions OR implies any oral hygiene instructions, nutritional or tobacco counseling, application of sealants to pits and fissures, silver diamine fluoride application, interim caries arresting medicament, oral cancer screening, caries risk assessment, or other non-restorative prevention procedures. INCLUDE this range if there's any suggestion of preventive care beyond routine cleaning and fluoride treatments.

## **Space Maintenance (D1510-D1555)**
**Use when:** Placing, repairing, or removing appliances designed to maintain space for erupting permanent teeth following premature loss of primary teeth.
**Check:** Documentation describes the type of space maintainer (fixed or removable), its location (unilateral or bilateral, maxillary or mandibular), and whether it's an initial placement, repair, or removal procedure.
**Note:** These devices (D1510-D1555) are critical in pediatric dentistry to preserve arch length and prevent malocclusion following early loss of primary teeth. Different codes apply based on design features, with special consideration for distal shoe appliances that guide unerupted first permanent molars.
**Activation trigger:** Scenario mentions OR implies any space maintainer placement, space maintenance following extraction or premature loss of primary teeth, band and loop appliance, lingual arch, transpalatal arch, distal shoe appliance, recementation of space maintainer, or removal of space maintainer. INCLUDE this range if there's any indication of managing space in a developing dentition after tooth loss.

## **Vaccinations (D1701-D1707)**
**Use when:** Administering vaccines in the dental setting to prevent diseases with oral manifestations or connection to oral health.
**Check:** Documentation confirms the type of vaccine administered, patient consent, and compliance with state regulations allowing dentists to administer vaccines.
**Note:** These codes (D1701-D1707) represent an expanding area of dental practice focused on preventing diseases with oral connections, such as HPV-related oropharyngeal cancers. Not all jurisdictions permit dentists to administer vaccines.
**Activation trigger:** Scenario mentions OR implies any administration of vaccines by dental providers, HPV vaccination, vaccine administration to prevent oral disease, dental practice-based immunization, or counseling related to vaccines that prevent oral or oropharyngeal conditions. INCLUDE this range if there's any reference to vaccination services provided in a dental setting.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_preventive(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing preventive scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Preventive analyze_preventive result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_preventive: {str(e)}")
            return ""
    
    async def activate_preventive(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            preventive_result = self.analyze_preventive(scenario)
            if not preventive_result:
                print("No preventive result returned")
                return {}
            
            print(f"Preventive Result in activate_preventive: {preventive_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, preventive_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": preventive_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in preventive analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_preventive(scenario)
        print(f"\n=== PREVENTIVE ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

preventive_service = PreventiveServices()
# Example usage
if __name__ == "__main__":
    async def main():
        preventive_service = PreventiveServices()
        scenario = input("Enter a preventive dental scenario: ")
        await preventive_service.run_analysis(scenario)
    
    asyncio.run(main())