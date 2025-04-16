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

class DiagnosticImagingServices:
    """Class to analyze and extract diagnostic imaging codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing diagnostic imaging."""
        return PromptTemplate(
            template=f"""
# Radiographic and Imaging Code Usage Guidelines

## 1. Determine the Imaging Purpose
- General dental exam? → D0210 (full mouth series), D0272 -(bitewings)
- Localized pain or pathology? → D0220 + D0230 (periapicals)
- TMJ or complex jaw issues? → D0320-D0322, D0368, D0384
- Surgical/implant planning? → CBCT codes D0364-D0367
- Orthodontic records? → D0330 (panoramic), D0340 (cephalometric), D0350 (photos)

## 2. Differentiate Between Capture and Interpretation
- If the image is captured but **not interpreted by the same provider**, use:
  - **D0701-D0709** for image capture only
  - **D0391** for interpretation by a different practitioner

## 3. Do Not Double Bill
- Don't bill both D0210 and individual component codes (e.g., D0220, D0274)
- If using D0372 (tomosynthesis full-mouth), don't also report D0210

## 4. Match the Right Imaging Code Type
- **2D Standard Radiographs:** D0210-D0277
- **Extraoral 2D Projections:** D0250-D0251
- **Panoramic:** D0330 (capture + interpretation), D0701 (capture only)
- **Cephalometric:** D0340 (capture + interpretation), D0702 (capture only)
- **Photographic Images:** D0350 (capture + interpretation), D0703 (capture only)
- **Tomosynthesis (layered digital images):** D0372-D0374 and D0387-D0389
- **CBCT:**  
  - Capture + interpretation → D0364-D0368  
  - Capture only → D0380-D0384  
- **MRI/Ultrasound:**  
  - Capture + interpretation → D0369-D0370  
  - Capture only → D0385-D0386  

## 5. Teledentistry & Mobile Visits
- Use D070X series when a hygienist or assistant takes the image offsite
- Pair with **D0391** if the dentist interprets it remotely
- Document clearly who captured and who interpreted

## 6. Advanced Functions
- **D0393** - Virtual treatment simulation (e.g., implant/ortho planning)
- **D0394** - Digital subtraction for tracking changes
- **D0395** - Fusion of multiple 3D images (e.g., CT + MRI)
- **D0801-D0804** - 3D surface scans for CAD/CAM, esthetics, or prosthetics

## 7. Documentation Must Include:
- Who captured and who interpreted the image
- Type of image and purpose (e.g., caries, implant planning)
- Interpretation results if applicable
- Whether a report was generated (especially for D0391, D0321, D0369)

Code: D0210  
Use when: A comprehensive intraoral radiographic series is needed to evaluate all teeth and surrounding bone, including edentulous areas. Commonly used during new patient exams, treatment planning for extensive restorations, periodontal evaluations, or when significant oral pathology is suspected.  
What to check: Ensure inclusion of both periapical and bitewing/interproximal images. Typically includes 14-22 images. Do not bill separately for individual images included in the series.

Code: D0220  
Use when: Capturing the first periapical radiographic image to evaluate the apex or root of a specific tooth. Common for assessing pain, trauma, or pathology in a localized area.  
What to check: Only report this once per date of service. Any additional periapical images must be reported under D0230.

Code: D0230  
Use when: Capturing each additional periapical image beyond the first during a single visit. Often required for multi-rooted teeth or when evaluating adjacent teeth.  
What to check: Must be used in conjunction with D0220. Report one unit per image.

Code: D0240  
Use when: Taking an occlusal radiographic image to visualize a broad cross-section of the arch. Useful in pediatric dentistry, detecting supernumerary teeth, impacted canines, or pathology in the palate/floor of the mouth.  
What to check: Specify maxillary or mandibular occlusal view. Rare in routine adult practice.

Code: D0250  
Use when: Capturing extra-oral 2D projection images using a stationary source/detector setup. Includes views such as lateral skull, PA skull, submentovertex, and Waters projection. Often used in ortho, oral surgery, and TMJ evaluations.  
What to check: Confirm image type and diagnostic purpose. Not to be confused with panoramic imaging.

Code: D0251  
Use when: Capturing a non-derived extra-oral image focused exclusively on the posterior teeth in both dental arches. May be used when intraoral imaging is not feasible.  
What to check: Ensure the image is original, not reconstructed from another radiographic source. Must clearly capture posterior dentition in both arches.

Code: D0270  
Use when: A single bitewing image is taken to detect interproximal caries or monitor alveolar bone levels. Common in pediatric or limited adult cases.  
What to check: Specify whether the image is on the right or left side. Do not use if multiple bitewings are taken.

Code: D0272  
Use when: Two bitewing images are taken, typically one on the left and one on the right side.  
What to check: This is the standard radiographic procedure during adult recall exams with no clinical caries and no high-risk factors. Confirm both sides are captured and visible.

Code: D0273  
Use when: Three bitewing images are needed, usually due to anatomical considerations such as a larger arch or spacing between posterior teeth.  
What to check: Ensure all interproximal surfaces of the posterior teeth are clearly captured. Consider documenting anatomical necessity.

Code: D0274  
Use when: Four bitewing images are taken to provide a more detailed and complete view of the interproximal areas.  
What to check: Confirm that all quadrants are covered—upper and lower left, upper and lower right. Often used in comprehensive exams.

Code: D0277  
Use when: Vertical bitewing series, typically 7-8 images, are taken to evaluate periodontal bone levels.  
What to check: Must document periodontal diagnosis or concern. Clarify that this is not part of a full-mouth radiographic series. Include clinical notes supporting periodontal need.

Code: D0310  
Use when: Sialography is performed to visualize salivary gland ductal anatomy and evaluate salivary flow or obstructions.  
What to check: Ensure the use of contrast media is documented along with procedural details. Record any anomalies found in ductal systems.

Code: D0320  
Use when: A TMJ arthrogram is performed, which includes the injection of contrast material followed by imaging.  
What to check: Documentation should include consent for contrast injection, the procedure details, and interpretation of images.

Code: D0321  
Use when: Radiographic imaging of the TMJ is done without the use of contrast material.  
What to check: Requires a narrative indicating the reason for TMJ imaging. Justify the need based on symptoms such as pain, dysfunction, or audible joint sounds.

Code: D0322  
Use when: A tomographic radiographic survey is done, which produces slice images, often for precise evaluation.  
What to check: Commonly used in implant planning or advanced TMJ analysis. Indicate the area of interest and rationale for tomography.

Code: D0330  
Use when: A panoramic radiograph is taken to assess a broad view of the jaws, teeth, nasal sinuses, and surrounding structures.  
What to check: Should include both maxilla and mandible. Confirm visibility of third molars, condyles, and sinuses. Ensure use is justified for diagnosis, treatment planning, or evaluation of pathology.

Code: D0340  
Use when: A 2D cephalometric radiograph is taken, typically for orthodontic or orthognathic surgical planning.  
What to check: Must include accurate patient positioning using a cephalostat. Confirm the capture of anatomical landmarks for analysis. Interpretative notes should detail skeletal relationships and support treatment objectives.

Code: D0350  
Use when: Taking diagnostic 2D facial or intraoral photos for documentation or case planning. Common uses include pre- and post-treatment records, orthodontic progress tracking, esthetic evaluations, and monitoring of lesions or soft tissue abnormalities.  
What to check: Document purpose clearly and ensure images are stored as part of the patient's record.

Code: D0364  
Use when: Capturing and interpreting CBCT with limited field of view (<1 jaw). Commonly used for evaluating impacted teeth, localized lesions, or single implant planning.  
What to check: Specify the anatomical region imaged (e.g., anterior mandible, posterior maxilla). Must include documented interpretation as part of the clinical record.

Code: D0365  
Use when: Capturing and interpreting CBCT of one full dental arch - mandible.  
What to check: Ensure interpretation included.

Code: D0366  
Use when: Capturing and interpreting CBCT of one full dental arch - maxilla, with or without cranium.  
What to check: Common for implant planning.

Code: D0367  
Use when: Capturing and interpreting CBCT of both jaws, with or without cranium.  
What to check: For ortho, full mouth rehab or surgical planning.

Code: D0368  
Use when: CBCT for TMJ series with 2 or more exposures.  
What to check: Specify bilateral TMJ imaging and include interpretation.

Code: D0369  
Use when: Performing and interpreting maxillofacial MRI.  
What to check: Document area studied and clinical reason.

Code: D0370  
Use when: Performing and interpreting maxillofacial ultrasound.  
What to check: Common for evaluating salivary glands or soft tissues.

Code: D0371  
Use when: Capturing and interpreting images during sialendoscopy.  
What to check: Image-based endoscopy of salivary ducts.

Code: D0372  
Use when: Performing intraoral tomosynthesis comprehensive series. This technique creates layered 3D-like images of the mouth by capturing multiple slices, offering more detailed visualization of the structures compared to standard 2D radiographs.  
What to check: Tomographic equivalent of D0210. Ideal for cases requiring higher diagnostic clarity, such as evaluating root fractures or complex anatomical features.

Code: D0373  
Use when: Capturing tomographic bitewing image.  
What to check: For enhanced interproximal caries or bone visualization.

Code: D0374  
Use when: Capturing tomographic periapical image.  
What to check: Digital imaging of specific teeth and periapical region.

Code: D0380  
Use when: Capturing CBCT image (no interpretation) with limited field (<1 jaw).  
What to check: Pair with D0391 if interpreted separately.

Code: D0381  
Use when: Capturing CBCT image (no interpretation) of full mandibular arch.  
What to check: Field limited to mandible.

Code: D0382  
Use when: Capturing CBCT image (no interpretation) of maxillary arch, with/without cranium.  
What to check: Document full arch.

Code: D0383  
Use when: Capturing CBCT of both jaws, no interpretation.  
What to check: Full field for ortho or complex diagnostics.

Code: D0384  
Use when: CBCT TMJ series (capture only), 2+ exposures.  
What to check: Requires separate interpretation code.

Code: D0385  
Use when: Capturing maxillofacial MRI only.  
What to check: Pair with D0391 if interpreted separately.

Code: D0386  
Use when: Capturing ultrasound image of maxillofacial area.  
What to check: Use with soft tissue pathology.

Code: D0387  
Use when: Capturing intraoral tomosynthesis comprehensive series (no interpretation).  
What to check: Similar to D0210 capture only.

Code: D0388  
Use when: Capturing bitewing tomosynthesis image only.  
What to check: Document number of views.

Code: D0389  
Use when: Capturing periapical tomosynthesis image only.  
What to check: Specific tooth and periapical anatomy.

Code: D0701  
Use when: Capturing panoramic image only (e.g., by hygienist or in off-site/mobile settings). This code is appropriate when the image is acquired but not interpreted by the same provider.  
What to check: Particularly relevant in teledentistry scenarios. The interpretation should be billed separately using D0391 if performed by a different provider.

Code: D0702  
Use when: Capturing cephalometric image only.  
What to check: Common in ortho setups.

Code: D0703  
Use when: Capturing 2D oral/facial photographs only.  
What to check: Use for documentation/monitoring.

Code: D0704  
Use when: Capturing 3D photographic image.  
What to check: Used for digital facial analysis.

Code: D0705  
Use when: Capturing extra-oral posterior dental image (capture only).  
What to check: Document imaging purpose.

Code: D0706  
Use when: Capturing intraoral occlusal image only.  
What to check: Document arch imaged.

Code: D0707  
Use when: Capturing intraoral periapical image only.  
What to check: Document tooth/area.

Code: D0708  
Use when: Capturing intraoral bitewing image only.  
What to check: Document number captured.

Code: D0709  
Use when: Capturing intraoral complete series (capture only).  
What to check: Interpretation billed separately.

Code: D0391  
Use when: Interpretation and report of diagnostic images by practitioner not associated with image capture. Examples include teledentistry consultations, specialty referrals, or scenarios where imaging technicians capture the images for later review by a dentist.  
What to check: Must document the interpretation and generate a written report that becomes part of the patient's record. Only use when the interpreter did not also capture the image.

Code: D0393  
Use when: Treatment simulation using 3D image volume. This may include implant placement simulation, orthodontic treatment simulation, or surgical simulation.  
What to check: Typically requires specialized software. Should include documentation of simulation parameters and objectives. Must go beyond basic CBCT interpretation. Excludes actual guide fabrication.

Code: D0394  
Use when: Digital subtraction of radiographic images. Used to track subtle changes in bone density or lesion progression over time.  
What to check: Requires original baseline images and follow-up images. Documentation should indicate changes observed through digital subtraction. Typically used in periodontal or implant monitoring.

Code: D0395  
Use when: Fusion of two or more 3D image volumes of same or different modalities. Examples include merging CBCT with digital models or facial scans.  
What to check: Document the purpose and clinical benefit of image fusion. Requires specialized software. Should enhance diagnosis or treatment planning beyond individual image interpretation.

Code: D0801  
Use when: 3D dental surface scan - direct. Used for digital impressions captured directly in the patient's mouth.  
What to check: Distinguish from traditional impressions. Document the clinical purpose for the scan.

Code: D0802  
Use when: 3D dental surface scan - indirect. Used when scanning dental models or impressions rather than directly scanning the oral cavity.  
What to check: Document the source of the physical model or impression. Indicate purpose for digitization.

Code: D0803  
Use when: 3D facial surface scan - direct. Used for capturing digital models of facial structures directly from the patient.  
What to check: Document the purpose (e.g., esthetic planning, surgical planning). Specify regions scanned.

Code: D0804  
Use when: 3D facial surface scan - indirect. Used for digitizing existing facial moulage or similar physical representations.  
What to check: Document the source of the physical model. Indicate the diagnostic or treatment planning purpose.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_diagnostic_imaging_code(self, scenario: str) -> str:
        """Extract diagnostic imaging code(s) for a given scenario."""
        try:
            print(f"Analyzing diagnostic imaging scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Diagnostic imaging extract_diagnostic_imaging_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in diagnostic imaging code extraction: {str(e)}")
            return ""
    
    def activate_diagnostic_imaging(self, scenario: str) -> str:
        """Activate the diagnostic imaging analysis process and return results."""
        try:
            result = self.extract_diagnostic_imaging_code(scenario)
            if not result:
                print("No diagnostic imaging code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating diagnostic imaging analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_diagnostic_imaging(scenario)
        print(f"\n=== DIAGNOSTIC IMAGING ANALYSIS RESULT ===")
        print(f"DIAGNOSTIC IMAGING CODE: {result if result else 'None'}")

diagnostic_imaging_service = DiagnosticImagingServices()
# Example usage
if __name__ == "__main__":
    imaging_service = DiagnosticImagingServices()
    scenario = input("Enter a diagnostic imaging dental scenario: ")
    imaging_service.run_analysis(scenario)