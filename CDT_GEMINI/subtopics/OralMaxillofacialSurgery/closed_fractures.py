"""
Module for extracting treatment of closed fractures codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class ClosedFracturesServices:
    """Class to analyze and extract closed fractures treatment codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing closed fractures treatment scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in oral and maxillofacial trauma management,

## **Closed Fractures Treatment**

### **Before picking a code, ask:**
- Which anatomical structure is fractured (maxilla, mandible, malar, zygomatic arch, alveolus)?
- Is an open or closed reduction technique being used for treatment?
- Are teeth present in the fracture line that require immobilization?
- Does the fracture treatment involve multiple surgical approaches?
- Is fixation required for the fracture treatment? If yes, what type?
- Is the fracture simple or comminuted (multiple fragments)?
- Does the treatment involve bone grafting or other complex reconstruction?
- Which specific regions of the facial bones are involved?
- Is there a need for interdisciplinary management with other specialists?
- What imaging was used to confirm and characterize the fracture?

---
#### **Code: D7610** – *Maxilla - open reduction (teeth immobilized, if present)*
**Use when:** Treating a fracture of the maxilla that requires surgical exposure of the fracture site, direct visualization, manipulation of the fracture fragments, and internal or external fixation to stabilize the segments.
**Check:** Documentation must clearly describe the incision made to expose the fracture, the method of reduction, and how the teeth (if present) were immobilized (wired, banded, or splinted).
**Note:** This procedure is more invasive than closed reduction and typically necessary for displaced or unstable maxillary fractures. The operative report should detail the surgical approach, exposure technique, method of fracture reduction, type of fixation (plates, screws, wires), and management of any teeth in the fracture line. Post-operative care instructions and follow-up plans are particularly important for monitoring healing and occlusal stability.

#### **Code: D7620** – *Maxilla - closed reduction (teeth immobilized, if present)*
**Use when:** Treating a maxillary fracture without surgical exposure of the fracture site, typically using manual manipulation and dental appliances or intermaxillary fixation to achieve reduction and stabilization.
**Check:** Verify documentation shows that fracture reduction was achieved without incision, typically through manipulation and external stabilization techniques.
**Note:** This less invasive approach is appropriate for non-displaced or minimally displaced fractures where anatomic reduction can be achieved without direct visualization of the fracture line. The procedure notes should document the method of manipulation, verification of reduction (usually radiographic), and the specific technique used for immobilization such as arch bars, intermaxillary fixation screws, or splints. If interosseous fixation is applied, code D7610 would be more appropriate.

#### **Code: D7630** – *Mandible - open reduction (teeth immobilized, if present)*
**Use when:** Performing reduction of a mandibular fracture that requires surgical exposure, direct visualization of the fracture site, and internal fixation of the fragments.
**Check:** Documentation should include the specific incisional approach (intraoral vs. extraoral), method of fracture exposure, reduction technique, and fixation method.
**Note:** Open reduction of mandibular fractures often involves more complex surgical planning due to the mandible's mobility and the presence of the inferior alveolar neurovascular bundle. The operative report should detail the precautions taken to protect vital structures, the specific hardware used for fixation, verification of anatomic reduction, and confirmation of normal occlusion. For bilateral or multiple fractures, each fracture should be described separately in the documentation.

#### **Code: D7640** – *Mandible - closed reduction (teeth immobilized, if present)*
**Use when:** Treating a mandibular fracture without surgical exposure, using manual manipulation followed by external stabilization through dental appliances or maxillomandibular fixation.
**Check:** Documentation must confirm that no incision was made to access the fracture site and detail the method used to achieve and maintain reduction.
**Note:** This approach is typically limited to non-displaced or minimally displaced mandibular fractures where anatomic alignment can be achieved through manual manipulation. The documentation should describe how reduction was verified (clinical and radiographic assessment), the specific method of immobilization (arch bars, intermaxillary elastics, splints), and the plan for monitoring healing progression. If interosseous fixation is needed, code D7630 would be more appropriate.

#### **Code: D7650** – *Malar and/or zygomatic arch - open reduction*
**Use when:** Performing surgical exposure and reduction of a fractured malar (cheek) bone or zygomatic arch with internal or external fixation.
**Check:** Documentation should detail the specific surgical approach, method of reduction, and fixation technique used for the malar or zygomatic arch fracture.
**Note:** These fractures often require careful reconstruction to maintain facial symmetry and proper projection of the cheek. The operative report should include the surgical approach (often coronal, intraoral, or limited incisions), method of fracture visualization, reduction technique, stabilization method, and verification of proper anatomic positioning. Assessment of infraorbital nerve function and globe position should be documented both pre- and post-operatively.

#### **Code: D7660** – *Malar and/or zygomatic arch - closed reduction*
**Use when:** Reducing a zygomatic arch or malar fracture without surgical exposure, typically using percutaneous techniques or extraoral pressure to elevate and realign the fracture.
**Check:** Ensure documentation shows the fracture was reduced without creating surgical access to the fracture site itself.
**Note:** Closed reduction of zygomatic arch fractures may involve techniques such as the Gillies approach (temporal incision for instrument insertion) or direct percutaneous manipulation using specialized instruments or digital pressure. Even though a small incision may be made for instrument access, it's considered closed reduction if the fracture site itself is not exposed. Documentation should include the specific technique, confirmation of reduction, and assessment of facial contour restoration.

#### **Code: D7670** – *Alveolus - closed reduction, may include stabilization of teeth*
**Use when:** Treating a fracture of the alveolar process without surgical exposure, usually involving manipulation and stabilization of the attached teeth to serve as a means of reduction.
**Check:** Verify documentation of a fracture involving the tooth-bearing portion of the jaw that was treated without direct surgical exposure of the fracture line.
**Note:** Alveolar fractures typically involve the portion of bone that supports the teeth. Treatment often focuses on reestablishing proper occlusion and stabilizing the segments through splinting, wiring, or bonding of the involved teeth. The procedure note should detail how the fragments were manipulated into position, the method of dental stabilization, occlusal verification, and the approach to managing any loose or avulsed teeth within the fracture segment.

#### **Code: D7671** – *Alveolus - open reduction, may include stabilization of teeth*
**Use when:** Treating an alveolar fracture through surgical exposure of the fracture site, direct visualization, reduction of the fragments, and internal fixation in addition to possible dental stabilization.
**Check:** Documentation must describe the surgical access to the alveolar fracture, visualization of the fracture line, and the method of direct reduction and fixation.
**Note:** This approach is necessary for significantly displaced alveolar fractures or those where closed reduction cannot achieve proper alignment. The surgical notes should detail the mucoperiosteal flap design, exposure of the fracture, reduction technique, method of osseous fixation (mini-plates, screws, wires), management of teeth in the fracture line, and verification of proper occlusal relationships. Post-operative care instructions should address both bone healing and dental concerns.

#### **Code: D7680** – *Facial bones - complicated reduction with fixation and multiple surgical approaches*
**Use when:** Managing complex facial fractures that involve multiple bones or require more than one surgical approach for adequate exposure, reduction, and fixation.
**Check:** Documentation must substantiate the complexity by detailing multiple surgical approaches and the various fixation methods required across different facial regions.
**Note:** This code applies to the most complex facial fracture patterns, such as panfacial fractures or those involving multiple midfacial buttresses, orbital floors, or nasoethmoidal regions. The comprehensive operative report should detail each surgical approach, the sequence of reduction and fixation, the hardware used at each location, methods to confirm proper anatomic relationships, and the rationale for the selected treatment sequence. Often, pre- and post-operative 3D imaging documentation is beneficial to demonstrate the reconstruction achieved.

---

### **Key Takeaways:**
- **Open vs. Closed Approach** - The key distinction between many code pairs is whether surgical exposure of the fracture site was required (open) or if treatment was accomplished without directly visualizing the fracture line (closed).
- **Anatomical Specificity** - Proper code selection requires precise identification of the fractured anatomical structure (maxilla, mandible, malar, zygomatic arch, alveolus).
- **Dental Considerations** - When teeth are present in the fracture line, documentation should address how they were managed and stabilized.
- **Fixation Methods** - Documentation should specify whether internal fixation (plates, screws, wires) or external fixation (arch bars, MMF) was used.
- **Occlusal Verification** - For fractures affecting tooth-bearing areas, documentation should confirm restoration of proper occlusal relationships.
- **Complexity Factors** - Code D7680 requires specific documentation of multiple surgical approaches and fixation methods across different facial regions.
- **Imaging Correlation** - Pre- and post-operative imaging should be referenced to document the nature of the fracture and verification of reduction.
- **Neurovascular Assessment** - Documentation should include evaluation of relevant neurosensory and vascular function before and after treatment.
- **Surgical Planning** - For complex cases, the treatment sequence and rationale should be clearly documented.
- **Follow-up Protocol** - Post-operative care instructions and follow-up plans are essential components of complete documentation.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_closed_fractures_code(self, scenario: str) -> str:
        """Extract closed fractures treatment code for a given scenario."""
        try:
            print(f"Analyzing closed fractures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Closed fractures extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_closed_fractures_code: {str(e)}")
            return ""
    
    def activate_closed_fractures(self, scenario: str) -> str:
        """Activate the closed fractures treatment analysis process and return results."""
        try:
            return self.extract_closed_fractures_code(scenario)
        except Exception as e:
            print(f"Error in activate_closed_fractures: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_closed_fractures(scenario)
        print(f"\n=== CLOSED FRACTURES TREATMENT ANALYSIS RESULT ===")
        print(f"CLOSED FRACTURES TREATMENT CODE: {result if result else 'None'}")


closed_fractures_service = ClosedFracturesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a closed fractures treatment scenario: ")
    closed_fractures_service.run_analysis(scenario) 