import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_diagnostic_imaging_extractor(temperature=0.0):   
    """
    Create a LangChain-based Diagnostic Imaging extractor.
    """
    # Use ChatOpenAI for newer models like gpt-4o
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=temperature)
    
    prompt_template = PromptTemplate(
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
- Don’t bill both D0210 and individual component codes (e.g., D0220, D0274)
- If using D0372 (tomosynthesis full-mouth), don’t also report D0210

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
What to check: Ensure inclusion of both periapical and bitewing/interproximal images. Typically includes 14-22 images. Do not bill separately for individual images included in the series. to evaluate all teeth and surrounding bone, including edentulous areas.  
What to check: Ensure inclusion of periapical and interproximal images for a full diagnostic overview.

Code: D0220  
Use when: Capturing the first periapical radiographic image to evaluate the apex or root of a specific tooth. Common for assessing pain, trauma, or pathology in a localized area.  
What to check: Only report this once per date of service. Any additional periapical images must be reported under D0230. during a diagnostic session.  
What to check: Must be followed by D0230 if additional periapicals are taken.

Code: D0230  
Use when: Capturing each additional periapical image beyond the first during a single visit. Often required for multi-rooted teeth or when evaluating adjacent teeth.  
What to check: Must be used in conjunction with D0220. Report one unit per image. after the first.  
What to check: Use one unit per image beyond the initial D0220.

Code: D0240  
Use when: Taking an occlusal radiographic image to visualize a broad cross-section of the arch. Useful in pediatric dentistry, detecting supernumerary teeth, impacted canines, or pathology in the palate/floor of the mouth.  
What to check: Specify maxillary or mandibular occlusal view. Rare in routine adult practice. to evaluate larger areas of the arch, especially in pediatric or trauma cases.  
What to check: Confirm indication for occlusal view.

Code: D0250  
Use when: Capturing extra-oral 2D projection images using a stationary source/detector setup. Includes views such as lateral skull, PA skull, submentovertex, and Waters projection. Often used in ortho, oral surgery, and TMJ evaluations.  
What to check: Confirm image type and diagnostic purpose. Not to be confused with panoramic imaging. like lateral skull, PA skull, or similar.  
What to check: Verify fixed source and detector; not panoramic.

Code: D0251  
Use when: Capturing a non-derived extra-oral image focused exclusively on the posterior teeth in both dental arches. May be used when intraoral imaging is not feasible.  
What to check: Ensure the image is original, not reconstructed from another radiographic source. Must clearly capture posterior dentition in both arches. in both arches.  
What to check: This image must be original and not reconstructed.

Code: D0270  
Use when: A single bitewing image is taken to detect interproximal caries or monitor alveolar bone levels. Common in pediatric or limited adult cases.  
What to check: Specify whether the image is on the right or left side. Do not use if multiple bitewings are taken. to assess interproximal caries or bone level.  
What to check: Indicate laterality if applicable.

Canvas Code: D0272  
**Use when**: Two bitewing images are taken, typically one on the left and one on the right side.  
**What to check**: This is the standard radiographic procedure during adult recall exams with no clinical caries and no high-risk factors. Confirm both sides are captured and visible.

Canvas Code: D0273  
**Use when**: Three bitewing images are needed, usually due to anatomical considerations such as a larger arch or spacing between posterior teeth.  
**What to check**: Ensure all interproximal surfaces of the posterior teeth are clearly captured. Consider documenting anatomical necessity.

Canvas Code: D0274  
**Use when**: Four bitewing images are taken to provide a more detailed and complete view of the interproximal areas.  
**What to check**: Confirm that all quadrants are covered—upper and lower left, upper and lower right. Often used in comprehensive exams.

Canvas Code: D0277  
**Use when**: Vertical bitewing series, typically 7-8 images, are taken to evaluate periodontal bone levels.  
**What to check**: Must document periodontal diagnosis or concern. Clarify that this is not part of a full-mouth radiographic series. Include clinical notes supporting periodontal need.

Canvas Code: D0310  
**Use when**: Sialography is performed to visualize salivary gland ductal anatomy and evaluate salivary flow or obstructions.  
**What to check**: Ensure the use of contrast media is documented along with procedural details. Record any anomalies found in ductal systems.

Canvas Code: D0320  
**Use when**: A TMJ arthrogram is performed, which includes the injection of contrast material followed by imaging.  
**What to check**: Documentation should include consent for contrast injection, the procedure details, and interpretation of images.

Canvas Code: D0321  
**Use when**: Radiographic imaging of the TMJ is done without the use of contrast material.  
**What to check**: Requires a narrative indicating the reason for TMJ imaging. Justify the need based on symptoms such as pain, dysfunction, or audible joint sounds.

Canvas Code: D0322  
**Use when**: A tomographic radiographic survey is done, which produces slice images, often for precise evaluation.  
**What to check**: Commonly used in implant planning or advanced TMJ analysis. Indicate the area of interest and rationale for tomography.

Canvas Code: D0330  
**Use when**: A panoramic radiograph is taken to assess a broad view of the jaws, teeth, nasal sinuses, and surrounding structures.  
**What to check**: Should include both maxilla and mandible. Confirm visibility of third molars, condyles, and sinuses. Ensure use is justified for diagnosis, treatment planning, or evaluation of pathology.

Canvas Code: D0340  
**Use when**: A 2D cephalometric radiograph is taken, typically for orthodontic or orthognathic surgical planning.  
**What to check**: Must include accurate patient positioning using a cephalostat. Confirm the capture of anatomical landmarks for analysis. Interpretative notes should detail skeletal relationships and support treatment objectives.

Code: D0350  
Use when: Taking diagnostic 2D facial or intraoral photos for documentation or case planning. Common uses include pre- and post-treatment records, orthodontic progress tracking, esthetic evaluations, and monitoring of lesions or soft tissue abnormalities.  
What to check: Document purpose clearly and ensure images are stored as part of the patient's record. for documentation or case planning.  
What to check: Document purpose (e.g., ortho, esthetics, lesions).

Code: D0364  
Use when: Capturing and interpreting CBCT with limited field of view (<1 jaw). Commonly used for evaluating impacted teeth, localized lesions, or single implant planning.  
What to check: Specify the anatomical region imaged (e.g., anterior mandible, posterior maxilla). Must include documented interpretation as part of the clinical record. (<1 jaw).  
What to check: Specify area imaged; must include interpretation.

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
What to check: Tomographic equivalent of D0210.

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
What to check: Particularly relevant in teledentistry scenarios. The interpretation should be billed separately using D0391 if performed by a different provider. (e.g., by hygienist).  
What to check: Interpretation billed separately.

Code: D0702  
Use when: Capturing cephalometric image only.  
What to check: Common in ortho setups.

Code: D0703  
Use when: Capturing 2D oral/facial photographs only.  
What to check: Use for documentation/monitoring.

Code: D0705  
Use when: Capturing posterior extraoral dental image only.  
What to check: Must be original and show posterior teeth in both arches.

Code: D0706  
Use when: Capturing occlusal intraoral image only.  
What to check: Often for pediatric or trauma eval.

Code: D0707  
Use when: Capturing periapical image only.  
What to check: Taken by non-dentist, no interpretation.

Code: D0708  
Use when: Capturing bitewing image only.  
What to check: Specify horizontal or vertical axis.

Code: D0709  
Use when: Capturing comprehensive intraoral series only.  
What to check: Taken offsite or by auxiliary, no interpretation.

Code: D0391  
Use when: Interpreting a diagnostic image captured by another provider.  
What to check: Must submit written report.

Code: D0393  
Use when: Running virtual treatment simulation using 3D data.  
What to check: Common for implant/ortho planning.

Code: D0394  
Use when: Performing digital subtraction of two or more images.  
What to check: Highlights progressive changes.

Code: D0395  
Use when: Fusing multiple 3D image volumes (e.g., CT + MRI).  
What to check: Used in complex surgical planning.

Code: D0801  
Use when: Capturing direct 3D surface scan on patient’s teeth.  
What to check: For CAD/CAM or ortho use.

Code: D0802  
Use when: Capturing indirect 3D dental surface scan (from model).  
What to check: Model must be labeled and retained.

Code: D0803  
Use when: Capturing 3D facial surface scan directly on patient.  
What to check: Used in facial esthetics, ortho.

Code: D0804  
Use when: Capturing indirect 3D facial scan (e.g., prosthetic mold).  
What to check: Scan from constructed features or prosthetics.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_diagnostic_imaging_code(scenario, temperature=0.0):
    """
    Extract Diagnostic Imaging code(s) for a given scenario.
    """
    chain = create_diagnostic_imaging_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_diagnostic_imaging(scenario):
    """
    Activate Diagnostic Imaging analysis and return results.
    """
    return extract_diagnostic_imaging_code(scenario)
