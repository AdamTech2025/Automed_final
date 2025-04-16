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
    from subtopics.Endodontics.apexification import apexification_service
    from subtopics.Endodontics.apicoectomy import apicoectomy_service
    from subtopics.Endodontics.endodonticretreatment import endodontic_retreatment_service
    from subtopics.Endodontics.endodontictherapy import endodontic_therapy_service
    from subtopics.Endodontics.otherendodontic import other_endodontic_service
    from subtopics.Endodontics.pulpcapping import pulpcapping_service
    from subtopics.Endodontics.pulpotomy import pulpotomy_service
    from subtopics.Endodontics.primaryteeth import primary_teeth_therapy_service
    from subtopics.Endodontics.pulpalregeneration import pulpal_regeneration_service
except ImportError:
    print("Warning: Could not import subtopics for Endodontics. Using fallback functions.")
    # Define fallback functions
    def activate_pulp_capping(scenario): return None
    def activate_pulpotomy(scenario): return None
    def activate_primary_teeth_therapy(scenario): return None
    def activate_endodontic_therapy(scenario): return None
    def activate_endodontic_retreatment(scenario): return None
    def activate_apexification(scenario): return None
    def activate_pulpal_regeneration(scenario): return None
    def activate_apicoectomy(scenario): return None
    def activate_other_endodontic(scenario): return None

class EndodonticServices:
    """Class to analyze and activate endodontic services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        self.registry.register("D3110-D3120", pulpcapping_service.activate_pulp_capping, 
                            "Pulp Capping (D3110-D3120)")
        self.registry.register("D3220-D3222", pulpotomy_service.activate_pulpotomy, 
                            "Pulpotomy (D3220-D3222)")
        self.registry.register("D3230-D3240", primary_teeth_therapy_service.activate_primary_teeth_therapy, 
                            "Endodontic Therapy on Primary Teeth (D3230-D3240)")
        self.registry.register("D3310-D3333", endodontic_therapy_service.activate_endodontic_therapy, 
                            "Endodontic Therapy (D3310-D3333)")
        self.registry.register("D3346-D3348", endodontic_retreatment_service.activate_endodontic_retreatment, 
                            "Endodontic Retreatment (D3346-D3348)")
        self.registry.register("D3351", apexification_service.activate_apexification, 
                            "Apexification/Recalcification (D3351)")
        self.registry.register("D3355-D3357", pulpal_regeneration_service.activate_pulpal_regeneration, 
                            "Pulpal Regeneration (D3355-D3357)")
        self.registry.register("D3410-D3470", apicoectomy_service.activate_apicoectomy, 
                            "Apicoectomy/Periradicular Services (D3410-D3470)")
        self.registry.register("D3910-D3999", other_endodontic_service.activate_other_endodontic, 
                            "Other Endodontic Procedures (D3910-D3999)")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing endodontic services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable endodontic code range(s) based on the following classifications:

## **Pulp Capping (D3110-D3120)**
**Use when:** Protecting exposed or nearly exposed pulp to preserve vitality.
**Check:** Documentation specifies direct or indirect pulp capping and materials used.
**Note:** These procedures aim to promote healing and prevent the need for root canal therapy.
**Activation trigger:** Scenario mentions OR implies any deep decay, pulp exposure, protective material placement, or efforts to maintain pulp vitality. INCLUDE this range if there's any indication of protecting the pulp from exposure or further damage.

## **Pulpotomy (D3220-D3222)**
**Use when:** Removing the coronal portion of pulp tissue while preserving radicular pulp.
**Check:** Documentation clearly indicates partial pulp removal and reason for procedure.
**Note:** Often performed on primary teeth or as an emergency procedure in permanent teeth.
**Activation trigger:** Scenario mentions OR implies any partial pulp removal, emergency pulpal treatment, or treatment of traumatic exposures. INCLUDE this range if there's any suggestion of coronal pulp removal or pain relief through pulp therapy.

## **Endodontic Therapy on Primary Teeth (D3230-D3240)**
**Use when:** Providing pulp therapy specifically for primary teeth.
**Check:** Documentation identifies primary teeth and specifies the pulpal treatment performed.
**Note:** These procedures are designed specifically for primary dentition with consideration for eventual exfoliation.
**Activation trigger:** Scenario mentions OR implies any primary tooth pulp treatment, pulpectomy in baby teeth, or root canal in deciduous teeth. INCLUDE this range if there's any indication of pulp therapy in a primary tooth.

## **Endodontic Therapy (D3310-D3333)**
**Use when:** Performing complete root canal treatment for permanent teeth.
**Check:** Documentation specifies the tooth treated and details of canal preparation and obturation.
**Note:** Different codes apply based on the tooth type (anterior, premolar, or molar).
**Activation trigger:** Scenario mentions OR implies any root canal treatment, pulpectomy, canal preparation, obturation, or treatment of irreversible pulpitis or necrosis. INCLUDE this range if there's any hint that complete endodontic therapy is needed or being performed.

## **Endodontic Retreatment (D3346-D3348)**
**Use when:** Redoing previously treated root canals that have failed.
**Check:** Documentation confirms previous endodontic treatment and reason for retreatment.
**Note:** These procedures involve removing previous filling materials and addressing issues like missed canals.
**Activation trigger:** Scenario mentions OR implies any failed root canal, persistent infection, retreatment, revision, or removal of previous canal fillings. INCLUDE this range if there's any suggestion that a tooth with previous endodontic treatment requires additional therapy.

## **Apexification/Recalcification (D3351)**
**Use when:** Treating immature permanent teeth with open apices.
**Check:** Documentation describes the tooth's developmental stage and material placement.
**Note:** These procedures promote apical closure in non-vital immature teeth.
**Activation trigger:** Scenario mentions OR implies any open apex, immature tooth with pulp necrosis, apical barrier placement, or calcium hydroxide/MTA procedures. INCLUDE this range if there's any indication of treating a non-vital tooth with incomplete root development.

## **Pulpal Regeneration (D3355-D3357)**
**Use when:** Attempting to regenerate pulp-dentin complex in immature necrotic teeth.
**Check:** Documentation details regenerative approach and materials used.
**Note:** These biologically-based procedures aim to continue root development.
**Activation trigger:** Scenario mentions OR implies any regenerative endodontic procedure, revascularization, blood clot induction, or stem cell approaches for immature teeth. INCLUDE this range if there's any suggestion of regenerative approaches rather than traditional apexification.

## **Apicoectomy/Periradicular Services (D3410-D3470)**
**Use when:** Performing surgical endodontic procedures to resolve periapical pathology.
**Check:** Documentation specifies the surgical approach, access, and root-end management.
**Note:** These procedures address cases where conventional root canal treatment is insufficient.
**Activation trigger:** Scenario mentions OR implies any periapical surgery, root-end resection, apicoectomy, retrograde filling, or persistent periapical pathology. INCLUDE this range if there's any indication that surgical intervention for endodontic issues is needed.

## **Other Endodontic Procedures (D3910-D3999)**
**Use when:** Performing specialized endodontic services not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the unusual or specialized procedure.
**Note:** These include procedures like tooth isolation, hemisection, or internal bleaching.
**Activation trigger:** Scenario mentions OR implies any specialized endodontic service, surgical exposure of root, internal bleaching, canal preparation for post, hemisection, or unclassified endodontic procedures. INCLUDE this range if there's any hint of endodontic procedures that don't clearly fit other categories.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_endodontic(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing endodontic scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Endodontics analyze_endodontic result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_endodontic: {str(e)}")
            return ""
    
    async def activate_endodontic(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            endodontic_result = self.analyze_endodontic(scenario)
            if not endodontic_result:
                print("No endodontic result returned")
                return {}
            
            print(f"Endodontic Result in activate_endodontic: {endodontic_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, endodontic_result)
            
            # Return a dictionary with the required fields
            return {
                "code_range": endodontic_result,
                "activated_subtopics": result["activated_subtopics"],
                "codes": result["topic_result"]
            }
        except Exception as e:
            print(f"Error in endodontic analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_endodontic(scenario)
        print(f"\n=== ENDODONTIC ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

endodontic_service = EndodonticServices()
# Example usage
if __name__ == "__main__":
    async def main():
        endo_service = EndodonticServices()
        scenario = input("Enter an endodontic dental scenario: ")
        await endo_service.run_analysis(scenario)
    
    asyncio.run(main())