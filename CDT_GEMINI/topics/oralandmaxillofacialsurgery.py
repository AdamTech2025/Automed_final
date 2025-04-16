import os
import sys
import asyncio
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

from sub_topic_registry import SubtopicRegistry

# Load environment variables
load_dotenv()

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Import modules
from topics.prompt import PROMPT

# Import service objects from subtopics with fallback mechanism
try:
    from subtopics.OralMaxillofacialSurgery.alveoloplasty import alveoloplasty_service
    from subtopics.OralMaxillofacialSurgery.excision_soft_tissue import excision_soft_tissue_service
    from subtopics.OralMaxillofacialSurgery.excision_intra_osseous import excision_intra_osseous_service
    from subtopics.OralMaxillofacialSurgery.excision_bone_tissue import excision_bone_tissue_service
    from subtopics.OralMaxillofacialSurgery.extractions import extractions_service
    from subtopics.OralMaxillofacialSurgery.closed_fractures import closed_fractures_service
    from subtopics.OralMaxillofacialSurgery.open_fractures import open_fractures_service
    from subtopics.OralMaxillofacialSurgery.other_surgical_procedures import other_surgical_procedures_service
    from subtopics.OralMaxillofacialSurgery.surgical_incision import surgical_incision_service
    from subtopics.OralMaxillofacialSurgery.tmj_dysfunctions import tmj_dysfunctions_service
    from subtopics.OralMaxillofacialSurgery.traumatic_wounds import traumatic_wounds_service
    from subtopics.OralMaxillofacialSurgery.complicated_suturing import complicated_suturing_service
    from subtopics.OralMaxillofacialSurgery.other_repair_procedures import other_repair_procedures_service
    from subtopics.OralMaxillofacialSurgery.vestibuloplasty import vestibuloplasty_service
    
except ImportError as e:
    print(f"Warning: Could not import subtopics for OralMaxillofacialSurgery: {str(e)}")
    print(f"Current sys.path: {sys.path}")
    # Define fallback functions
    def activate_extractions(scenario): return None
    def activate_other_surgical_procedures(scenario): return None
    def activate_alveoloplasty(scenario): return None
    def activate_vestibuloplasty(scenario): return None
    def activate_excision_soft_tissue(scenario): return None
    def activate_excision_intra_osseous(scenario): return None
    def activate_excision_bone_tissue(scenario): return None
    def activate_surgical_incision(scenario): return None
    def activate_closed_fractures(scenario): return None
    def activate_open_fractures(scenario): return None
    def activate_tmj_dysfunctions(scenario): return None
    def activate_traumatic_wounds(scenario): return None
    def activate_complicated_suturing(scenario): return None
    def activate_other_repair_procedures(scenario): return None

class OralMaxillofacialSurgeryServices:
    """Class to analyze and activate oral and maxillofacial surgery services based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        self.registry = SubtopicRegistry()
        self._register_subtopics()
    
    def _register_subtopics(self):
        """Register all subtopics for parallel activation."""
        try:
            self.registry.register("D7111-D7140", extractions_service.activate_extractions, 
                                "Extractions (D7111-D7140)")
            self.registry.register("D7210-D7251", extractions_service.activate_extractions, 
                                "Surgical Extractions (D7210-D7251)")
            self.registry.register("D7260-D7297", other_surgical_procedures_service.activate_other_surgical_procedures, 
                                "Other Surgical Procedures (D7260-D7297)")
            self.registry.register("D7310-D7321", alveoloplasty_service.activate_alveoloplasty, 
                                "Alveoloplasty (D7310-D7321)")
            self.registry.register("D7340-D7350", vestibuloplasty_service.activate_vestibuloplasty, 
                                "Vestibuloplasty (D7340-D7350)")
            self.registry.register("D7410-D7465", excision_soft_tissue_service.activate_excision_soft_tissue, 
                                "Excision of Soft Tissue Lesions (D7410-D7465)")
            self.registry.register("D7440-D7461", excision_intra_osseous_service.activate_excision_intra_osseous, 
                                "Excision of Intra-Osseous Lesions (D7440-D7461)")
            self.registry.register("D7471-D7490", excision_bone_tissue_service.activate_excision_bone_tissue, 
                                "Excision of Bone Tissue (D7471-D7490)")
            self.registry.register("D7510-D7560", surgical_incision_service.activate_surgical_incision, 
                                "Surgical Incision (D7510-D7560)")
            self.registry.register("D7610-D7780", closed_fractures_service.activate_closed_fractures, 
                                "Treatment of Closed Fractures (D7610-D7780)")
            self.registry.register("D7610-D7780", open_fractures_service.activate_open_fractures, 
                                "Treatment of Open Fractures (D7610-D7780)")
            self.registry.register("D7810-D7880", tmj_dysfunctions_service.activate_tmj_dysfunctions, 
                                "Reduction of Dislocation (D7810-D7880)")
            self.registry.register("D7910-D7912", traumatic_wounds_service.activate_traumatic_wounds, 
                                "Repair of Traumatic Wounds (D7910-D7912)")
            self.registry.register("D7911-D7912", complicated_suturing_service.activate_complicated_suturing, 
                                "Complicated Suturing (D7911-D7912)")
            self.registry.register("D7920-D7999", other_repair_procedures_service.activate_other_repair_procedures, 
                                "Other Repair Procedures (D7920-D7999)")
        except Exception as e:
            print(f"Error registering subtopics: {str(e)}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing oral and maxillofacial surgery services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable oral and maxillofacial surgery code range(s) based on the following classifications:

## IMPORTANT GUIDELINES:
- You should activate ALL code ranges that have any potential relevance to the scenario
- Even if a code range is only slightly related, include it in your response
- Only exclude a code range if it is DEFINITELY NOT relevant to the scenario
- When in doubt, INCLUDE the code range rather than exclude it
- Multiple code ranges can and should be activated if they have any potential applicability
- Your goal is to ensure no potentially relevant codes are missed

## **Extractions (D7111-D7140)**
**Use when:** Removing teeth through simple non-surgical procedures.
**Check:** Documentation indicates routine extraction without significant bone removal or sectioning.
**Note:** These are straightforward procedures typically performed with elevators and forceps.
**Activation trigger:** Scenario mentions OR implies any simple extraction, removal of erupted tooth, or non-surgical tooth removal. INCLUDE this range if there's any indication of basic tooth extraction without surgical intervention.

## **Surgical Extractions (D7210-D7251)**
**Use when:** Removing teeth that require surgical intervention.
**Check:** Documentation details flap elevation, bone removal, or tooth sectioning.
**Note:** These procedures are more complex than simple extractions and may involve impacted teeth.
**Activation trigger:** Scenario mentions OR implies any surgical extraction, removal of bone, sectioning of tooth, impacted tooth, or complicated extraction. INCLUDE this range if there's any hint of extraction requiring more than elevators and forceps.

## **Other Surgical Procedures (D7260-D7297)**
**Use when:** Performing specialized oral surgical procedures beyond extractions.
**Check:** Documentation specifies the exact procedure and anatomical structures involved.
**Note:** These include oroantral fistula closures, tooth reimplantation, surgical exposure, and biopsies.
**Activation trigger:** Scenario mentions OR implies any specialized oral surgery, fistula, reimplantation, exposure of unerupted teeth, or tissue biopsy. INCLUDE this range if there's any suggestion of oral surgical procedures beyond extractions.

## **Alveoloplasty (D7310-D7321)**
**Use when:** Surgically remodeling and smoothing bone after extractions.
**Check:** Documentation describes ridge preparation and whether performed with extractions or separately.
**Note:** These procedures prepare the ridge for prosthetic placement.
**Activation trigger:** Scenario mentions OR implies any bone recontouring, ridge smoothing, preparation for dentures, or alveolar ridge modification. INCLUDE this range if there's any suggestion of bone remodeling related to tooth extraction sites.

## **Vestibuloplasty (D7340-D7350)**
**Use when:** Surgically modifying the vestibular depth and soft tissues.
**Check:** Documentation specifies the surgical approach and graft materials if used.
**Note:** These procedures increase the vestibular depth for prosthetic stability.
**Activation trigger:** Scenario mentions OR implies any vestibular extension, soft tissue modification for dentures, ridge extension, or tissue grafting for prosthetic purposes. INCLUDE this range if there's any indication of surgical alteration of vestibular tissues.

## **Excision of Soft Tissue Lesions (D7410-D7465)**
**Use when:** Removing lesions or abnormal tissues from oral structures.
**Check:** Documentation details size, location, and pathology results of excised tissue.
**Note:** These procedures address pathological conditions requiring removal.
**Activation trigger:** Scenario mentions OR implies any tissue biopsy, lesion removal, excision of abnormal tissue, or removal of cysts or tumors. INCLUDE this range if there's any hint of removing pathological tissue from the oral cavity.

## **Excision of Intra-Osseous Lesions (D7440-D7461)**
**Use when:** Removing lesions within the bone.
**Check:** Documentation specifies the exact procedure, lesion type, and extent of bone involvement.
**Note:** These address pathological conditions within the jawbones.
**Activation trigger:** Scenario mentions OR implies any bony lesion, intraosseous cyst, jaw tumor, or pathology within bone. INCLUDE this range if there's any indication of lesions or pathology within the jawbones requiring surgical removal.

## **Excision of Bone Tissue (D7471-D7490)**
**Use when:** Removing excess bone or bony growths.
**Check:** Documentation identifies the specific bony structure and reason for removal.
**Note:** These procedures address non-pathological bony overgrowths or interferences.
**Activation trigger:** Scenario mentions OR implies any tori, exostosis, excessive bone, bony protuberance, or bone removal for prosthetic purposes. INCLUDE this range if there's any suggestion of removing excess bone not related to pathology.

## **Surgical Incision (D7510-D7560)**
**Use when:** Creating surgical openings to drain infections or remove foreign bodies.
**Check:** Documentation describes the reason for incision and what was drained or removed.
**Note:** These procedures address acute conditions requiring immediate drainage.
**Activation trigger:** Scenario mentions OR implies any incision and drainage, abscess treatment, swelling, infection, or foreign body removal. INCLUDE this range if there's any suggestion of creating a surgical opening for therapeutic purposes.

## **Treatment of Fractures (D7610-D7780)**
**Use when:** Managing facial or jaw fractures through surgical intervention.
**Check:** Documentation specifies fracture type, location, and fixation method.
**Note:** These procedures restore function and proper alignment after trauma.
**Activation trigger:** Scenario mentions OR implies any jaw fracture, facial trauma, bone plating, fixation of fragments, or fracture reduction. INCLUDE this range if there's any indication of treating broken facial or jaw bones.

## **Reduction of Dislocation (D7810-D7880)**
**Use when:** Correcting dislocated temporomandibular joint or managing TMJ dysfunction.
**Check:** Documentation details the condition and specific intervention performed.
**Note:** These procedures address joint-related conditions affecting function.
**Activation trigger:** Scenario mentions OR implies any TMJ disorder, jaw joint problems, clicking, locking, disc displacement, or joint manipulation. INCLUDE this range if there's any hint of temporomandibular joint issues requiring intervention.

## **Repair of Traumatic Wounds (D7910-D7912)**
**Use when:** Suturing or otherwise closing traumatic wounds.
**Check:** Documentation specifies wound size, complexity, and repair technique.
**Note:** These procedures address soft tissue injuries from trauma.
**Activation trigger:** Scenario mentions OR implies any laceration, soft tissue injury, suturing, wound closure, or traumatic tissue damage. INCLUDE this range if there's any suggestion of repairing damaged oral tissues after injury.

## **Complicated Suturing (D7911-D7912)**
**Use when:** Closing complex wounds requiring advanced techniques.
**Check:** Documentation details the complexity factors and closure method.
**Note:** These are more involved than simple suturing procedures.
**Activation trigger:** Scenario mentions OR implies any complex laceration, extensive tissue damage, complicated wound closure, or wounds requiring layered repair. INCLUDE this range if there's any indication of complex wound management beyond simple suturing.

## **Other Repair Procedures (D7920-D7999)**
**Use when:** Performing specialized surgical procedures not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the unusual or specialized procedure.
**Note:** These include skin grafts, sinus procedures, frenectomies, and other specialized surgeries.
**Activation trigger:** Scenario mentions OR implies any frenectomy, sinus procedures, skin grafts, bone replacement, specialized surgical interventions, or unusual maxillofacial procedures. INCLUDE this range if there's any hint of specialized surgical procedures not clearly fitting other categories.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
    
    def analyze_oral_maxillofacial_surgery(self, scenario: str) -> str:
        """Analyze the scenario to determine applicable code ranges."""
        try:
            print(f"Analyzing oral and maxillofacial surgery scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code_range = result.strip()
            print(f"Oral & Maxillofacial Surgery analyze_oral_maxillofacial_surgery result: {code_range}")
            return code_range
        except Exception as e:
            print(f"Error in analyze_oral_maxillofacial_surgery: {str(e)}")
            return ""
    
    async def activate_oral_maxillofacial_surgery(self, scenario: str) -> dict:
        """Activate relevant subtopics in parallel and return detailed results."""
        try:
            # Get the code range from the analysis
            oral_surgery_result = self.analyze_oral_maxillofacial_surgery(scenario)
            if not oral_surgery_result:
                print("No oral and maxillofacial surgery result returned")
                return {}
            
            print(f"Oral & Maxillofacial Surgery Result in activate_oral_maxillofacial_surgery: {oral_surgery_result}")
            
            # Activate subtopics in parallel using the registry
            result = await self.registry.activate_all(scenario, oral_surgery_result)
            
            # Initialize lists from registry results
            topic_result = result["topic_result"]
            activated_subtopics = result["activated_subtopics"]
            
            # Special case for sialoliths
            if "sialolith" in scenario.lower() and "D7260-D7297" not in oral_surgery_result:
                print("Activating subtopic: Other Surgical Procedures (D7260-D7297) - Sialolithotomy")
                code = other_surgical_procedures_service.activate_other_surgical_procedures(scenario)
                if code:
                    topic_result.append(code)
                    activated_subtopics.append("Other Surgical Procedures (D7260-D7297) - Sialolithotomy")
            
            # Return a dictionary with the required fields
            return {
                "code_range": oral_surgery_result,
                "activated_subtopics": activated_subtopics,
                "codes": topic_result
            }
        except Exception as e:
            print(f"Error in oral and maxillofacial surgery analysis: {str(e)}")
            return {}
    
    async def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = await self.activate_oral_maxillofacial_surgery(scenario)
        print(f"\n=== ORAL & MAXILLOFACIAL SURGERY ANALYSIS RESULT ===")
        print(f"CODE RANGE: {result.get('code_range', 'None')}")
        print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
        print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

oral_surgery_service = OralMaxillofacialSurgeryServices()
# Example usage
if __name__ == "__main__":
    async def main():
        oral_surgery_service = OralMaxillofacialSurgeryServices()
        scenario = input("Enter an oral and maxillofacial surgery scenario: ")
        await oral_surgery_service.run_analysis(scenario)
    
    asyncio.run(main())