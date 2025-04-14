"""
Module for extracting surgical periodontal services codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_surgical_services_extractor(temperature=0.0):
    """
    Create a LangChain-based surgical periodontal services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it for a periodontal condition requiring surgical intervention, or was it identified during a routine exam?
- How many teeth or tooth-bounded spaces are involved, and in which quadrant?
- Is the procedure addressing gingival tissue, bone, or both, and is it surgical or non-surgical?
- Are there specific periodontal findings (e.g., pocket depth, bone loss, inflammation) driving the treatment?
- Does the procedure involve additional steps like grafting, regeneration, or postoperative care that require separate coding?

---

### Surgical Services, Postoperative Care (Periodontics)

#### Code: D4210
**Heading:** Gingivectomy or gingivoplasty — four or more contiguous teeth or tooth bounded spaces per quadrant  
**Description:** Performed to eliminate suprabony pockets or restore normal architecture when gingival enlargements or asymmetrical/unaesthetic topography is evident with normal bony configuration.  
**When to Use:**  
- The patient has gingival overgrowth or suprabony pockets affecting four or more contiguous teeth/spaces in a quadrant, requiring surgical removal or reshaping.  
- Use for esthetic or functional correction with healthy underlying bone.  
**What to Check:**  
- Confirm ≥4 contiguous teeth/spaces via periodontal charting or exam.  
- Assess pocket depths and gingival condition (e.g., hyperplasia, asymmetry).  
- Check bone health (normal configuration) via radiograph.  
- Verify quadrant-specific treatment.  
**Notes:**  
- Not for osseous surgery (see D4260)—bone is not altered.  
- Narrative may be needed for insurance if esthetic-driven.  
- Use D4211 for fewer teeth.  

#### Code: D4211
**Heading:** Gingivectomy or gingivoplasty — one to three contiguous teeth or tooth bounded spaces per quadrant  
**Description:** Performed to eliminate suprabony pockets or restore normal architecture when gingival enlargements or asymmetrical/unaesthetic topography is evident with normal bony configuration.  
**When to Use:**  
- The patient has gingival issues on 1-3 contiguous teeth/spaces in a quadrant needing surgical correction.  
- Use for localized gingival overgrowth or esthetic adjustment.  
**What to Check:**  
- Confirm 1-3 contiguous teeth/spaces via exam or charting.  
- Assess gingival health and pocket depths.  
- Check bone status (normal) via radiograph.  
- Verify quadrant-specific application.  
**Notes:**  
- Not for bone-involved cases (see D4261).  
- Use D4210 for ≥4 teeth.  
- Documentation of necessity required for insurance.  

#### Code: D4212
**Heading:** Gingivectomy or gingivoplasty to allow access for restorative procedure, per tooth  
**When to Use:**  
- The patient requires gingival tissue removal on a single tooth to enable a restorative procedure (e.g., crown placement).  
- Use for access, not periodontal disease treatment.  
**What to Check:**  
- Confirm the tooth needs restorative work and gingival interference via exam.  
- Assess gingival overgrowth blocking access.  
- Check if paired with a restorative code (e.g., D2750).  
- Verify no broader periodontal surgery is needed.  
**Notes:**  
- Per-tooth code—not quadrant-based.  
- Narrative needed to link to restorative intent.  
- Not for general gingivectomy (see D4210/D4211).  

#### Code: D4230
**Heading:** Anatomical crown exposure — four or more contiguous teeth or bounded tooth spaces per quadrant  
**Description:** Removes enlarged gingival tissue and supporting bone (ostectomy) in a periodontally healthy area to provide an anatomically correct gingival relationship.  
**When to Use:**  
- The patient has ≥4 contiguous teeth/spaces needing crown exposure in a healthy periodontal environment (e.g., for esthetics or ortho).  
- Involves bone removal for proper gingival contour.  
**What to Check:**  
- Confirm ≥4 teeth/spaces and periodontal health via exam/radiograph.  
- Assess gingival enlargement and bone involvement.  
- Check for esthetic or functional goals.  
- Verify quadrant-specific treatment.  
**Notes:**  
- Not for diseased periodontium (see D4260).  
- Use D4231 for fewer teeth.  
- Requires X-rays for insurance justification.  

#### Code: D4231
**Heading:** Anatomical crown exposure — one to three contiguous teeth or bounded tooth spaces per quadrant  
**Description:** Removes enlarged gingival tissue and supporting bone (ostectomy) in a periodontally healthy area to provide an anatomically correct gingival relationship.  
**When to Use:**  
- The patient has 1-3 contiguous teeth/spaces needing crown exposure in a healthy periodontal area.  
- Use for localized bone and tissue adjustment.  
**What to Check:**  
- Confirm 1-3 teeth/spaces and healthy periodontium via exam/radiograph.  
- Assess need for ostectomy and gingival reshaping.  
- Check quadrant-specific application.  
- Verify no periodontal disease present.  
**Notes:**  
- Use D4230 for ≥4 teeth.  
- Not for periodontal disease treatment.  
- Documentation of health status critical for insurance.  

#### Code: D4240
**Heading:** Gingival flap procedure, including root planing — four or more contiguous teeth or tooth bounded spaces per quadrant  
**Description:** A soft tissue flap is reflected/resected for root debridement and granulation tissue removal, without osseous recontouring. Includes various flap techniques for moderate/deep pockets or diagnostic needs.  
**When to Use:**  
- The patient has ≥4 contiguous teeth/spaces with moderate to deep pockets requiring flap access for root planing.  
- Use for periodontal disease or diagnostic purposes (e.g., cracked tooth).  
**What to Check:**  
- Confirm ≥4 teeth/spaces and pocket depths via charting.  
- Assess attachment loss and need for root access via radiograph.  
- Check if osseous surgery is avoided (otherwise, see D4260).  
- Verify quadrant-specific treatment.  
**Notes:**  
- Includes root planing—don’t code D4341 separately.  
- Use D4241 for fewer teeth.  
- Narrative may detail flap type or diagnostic intent.  

#### Code: D4241
**Heading:** Gingival flap procedure, including root planing — one to three contiguous teeth or tooth bounded spaces per quadrant  
**Description:** A soft tissue flap is reflected/resected for root debridement and granulation tissue removal, without osseous recontouring. Includes various flap techniques for moderate/deep pockets or diagnostic needs.  
**When to Use:**  
- The patient has 1-3 contiguous teeth/spaces with pockets needing flap access for root planing.  
- Use for localized periodontal or diagnostic treatment.  
**What to Check:**  
- Confirm 1-3 teeth/spaces and pocket depths via charting.  
- Assess need for flap and root debridement via radiograph.  
- Check no bone recontouring is done (see D4261 if so).  
- Verify quadrant-specific application.  
**Notes:**  
- Includes root planing—don’t code D4342 separately.  
- Use D4240 for ≥4 teeth.  
- Documentation of pocket depth required.  

#### Code: D4245
**Heading:** Apically positioned flap  
**Description:** Used to preserve keratinized gingiva with osseous resection, second-stage implant procedures, or during surgical exposure of impacted teeth/treatment of peri-implantitis.  
**When to Use:**  
- The patient requires an apically positioned flap to maintain keratinized tissue during surgery (e.g., osseous work, implant exposure).  
- Use for specific periodontal or implant-related goals.  
**What to Check:**  
- Confirm need to preserve keratinized gingiva via exam.  
- Assess procedure context (e.g., osseous surgery, implant) via radiograph.  
- Check if paired with other codes (e.g., D4260).  
- Verify surgical site and intent.  
**Notes:**  
- Often an adjunct—document primary procedure.  
- Narrative needed for insurance (e.g., peri-implantitis).  
- Not for general flap procedures (see D4240).  

#### Code: D4249
**Heading:** Clinical crown lengthening — hard tissue  
**Description:** Allows restorative procedures on teeth with little exposed structure by reflecting a flap and removing bone, altering the crown-to-root ratio in a healthy periodontal environment.  
**When to Use:**  
- The patient has a tooth with insufficient crown exposure for restoration, requiring bone removal in a healthy periodontium.  
- Use for restorative access, not periodontal disease.  
**What to Check:**  
- Confirm restorative need and limited crown exposure via exam/radiograph.  
- Assess periodontal health (no disease) and bone removal extent.  
- Check if paired with restorative code (e.g., D2750).  
- Verify tooth-specific application.  
**Notes:**  
- Not for diseased periodontium (see D4260).  
- Narrative links to restorative goal for insurance.  
- Per-tooth code—don’t use quadrant codes.  

#### Code: D4260
**Heading:** Osseous surgery (including elevation of a full thickness flap and closure) — four or more contiguous teeth or tooth bounded spaces per quadrant  
**Description:** Modifies bony support by reshaping the alveolar process (ostectomy/osteoplasty) for periodontal disease treatment.  
**When to Use:**  
- The patient has ≥4 contiguous teeth/spaces with periodontal disease requiring bone reshaping and flap surgery.  
- Use for advanced bone defects.  
**What to Check:**  
- Confirm ≥4 teeth/spaces and bone loss via charting/radiograph.  
- Assess pocket depths and attachment loss.  
- Check ostectomy/osteoplasty is performed.  
- Verify quadrant-specific treatment.  
**Notes:**  
- Use D4261 for fewer teeth.  
- Additional procedures (e.g., grafts) coded separately.  
- Requires X-rays and perio charting for insurance.  

#### Code: D4261
**Heading:** Osseous surgery (including elevation of a full thickness flap and closure) — one to three contiguous teeth or tooth bounded spaces per quadrant  
**Description:** Modifies bony support by reshaping the alveolar process (ostectomy/osteoplasty) for periodontal disease treatment.  
**When to Use:**  
- The patient has 1-3 contiguous teeth/spaces with periodontal disease needing bone reshaping and flap surgery.  
- Use for localized bone defects.  
**What to Check:**  
- Confirm 1-3 teeth/spaces and bone loss via charting/radiograph.  
- Assess need for ostectomy/osteoplasty.  
- Check quadrant-specific application.  
- Verify periodontal disease presence.  
**Notes:**  
- Use D4260 for ≥4 teeth.  
- Separate codes for concurrent procedures.  
- Documentation of bone work critical.  

#### Code: D4263
**Heading:** Bone replacement graft — retained natural tooth — first site in quadrant  
**Description:** Uses grafts to stimulate periodontal regeneration for bone deformity from disease, excluding flap entry, debridement, or other regenerative steps.  
**When to Use:**  
- The patient has a periodontal bone defect on a natural tooth needing a graft at the first site in a quadrant.  
- Use for regeneration, not extraction sites.  
**What to Check:**  
- Confirm bone defect and retained tooth via radiograph.  
- Assess defect size and graft material.  
- Check if flap/debridement is separate (e.g., D4260).  
- Verify quadrant-specific first site.  
**Notes:**  
- Use D4264 for additional sites.  
- Not for edentulous areas—document tooth presence.  
- Narrative/X-rays required for insurance.  

#### Code: D4264
**Heading:** Bone replacement graft — retained natural tooth — each additional site in quadrant  
**Description:** Uses grafts for periodontal regeneration at additional sites, performed with D4263, excluding flap entry or other regenerative steps.  
**When to Use:**  
- The patient has additional bone defect sites in the same quadrant as D4263 needing grafts.  
- Use per extra site on retained teeth.  
**What to Check:**  
- Confirm D4263 is used and additional sites exist via radiograph.  
- Assess each site’s defect and graft need.  
- Check not for edentulous spaces.  
- Verify quadrant-specific application.  
**Notes:**  
- Not standalone—requires D4263.  
- Specify site count in documentation.  
- Insurance may scrutinize multi-site grafts.  

#### Code: D4265
**Heading:** Biologic materials to aid in soft and osseous tissue regeneration, per site  
**Description:** Uses biologic materials (e.g., growth factors) alone or with grafts/barriers for regeneration, excluding surgical entry or debridement.  
**When to Use:**  
- The patient has a periodontal defect needing biologic materials to enhance tissue regeneration at a specific site.  
- Use as an adjunct to surgery or grafts.  
**What to Check:**  
- Confirm defect and regeneration need via exam/radiograph.  
- Assess material type and site-specific application.  
- Check if paired with other codes (e.g., D4263).  
- Verify not including flap entry.  
**Notes:**  
- Separate from grafts (D4263)—focuses on biologics.  
- Narrative specifies material and purpose.  
- Insurance may require justification.  

#### Code: D4266
**Heading:** Guided tissue regeneration, natural teeth — resorbable barrier, per site  
**Description:** Uses a resorbable barrier for periodontal regeneration around natural teeth, excluding flap entry or other regenerative steps.  
**When to Use:**  
- The patient has a periodontal defect needing a resorbable barrier for guided tissue regeneration at a site.  
- Use for natural teeth only.  
**What to Check:**  
- Confirm defect and tooth presence via radiograph.  
- Assess barrier type (resorbable) and site need.  
- Check if flap/grafts are separate (e.g., D4260).  
- Verify site-specific application.  
**Notes:**  
- Use D4267 for non-resorbable barriers.  
- Narrative/X-rays needed for insurance.  
- Not for implants or edentulous areas.  

#### Code: D4267
**Heading:** Guided tissue regeneration, natural teeth — non-resorbable barrier, per site  
**Description:** Uses a non-resorbable barrier for periodontal regeneration around natural teeth, excluding flap entry or other regenerative steps.  
**When to Use:**  
- The patient has a periodontal defect needing a non-resorbable barrier for regeneration at a site.  
- Use for natural teeth only.  
**What to Check:**  
- Confirm defect and tooth presence via radiograph.  
- Assess barrier type (non-resorbable) and site need.  
- Check if flap/grafts are separate (e.g., D4260).  
- Verify site-specific application.  
**Notes:**  
- Use D4286 for barrier removal.  
- Narrative/X-rays required for insurance.  
- Not for resorbable barriers (see D4266).  

#### Code: D4286
**Heading:** Removal of non-resorbable barrier  
**When to Use:**  
- The patient requires surgical removal of a previously placed non-resorbable barrier (e.g., from D4267).  
- Use for follow-up procedure.  
**What to Check:**  
- Confirm prior D4267 use and barrier presence via record/radiograph.  
- Assess need for removal (e.g., healing complete).  
- Check surgical site condition.  
- Verify tooth-specific application.  
**Notes:**  
- Pairs with D4267—document prior placement.  
- Narrative explains timing and necessity.  
- Not for resorbable barriers (self-dissolving).  

#### Code: D4268
**Heading:** Surgical revision procedure, per tooth  
**Description:** Refines results of prior surgery by modifying hard/soft tissue contours, often with a flap.  
**When to Use:**  
- The patient needs revision of a previous periodontal surgery (e.g., irregular bone/soft tissue) on a specific tooth.  
- Use for refinement, not primary treatment.  
**What to Check:**  
- Confirm prior surgery and need for revision via exam/radiograph.  
- Assess tissue/bone irregularities.  
- Check if flap is elevated for access.  
- Verify tooth-specific application.  
**Notes:**  
- Per-tooth code—document prior procedure.  
- Narrative links to original surgery.  
- Not for initial periodontal surgery.  

#### Code: D4270
**Heading:** Pedicle soft tissue graft procedure  
**Description:** A pedicle flap of gingiva is moved laterally/coronally to replace mucosa or cover an exposed root.  
**When to Use:**  
- The patient has a gingival defect or exposed root needing a pedicle graft from adjacent tissue.  
- Use for coverage or augmentation.  
**What to Check:**  
- Confirm defect/root exposure and donor site via exam.  
- Assess pedicle feasibility (e.g., adjacent gingiva).  
- Check esthetic/functional goals.  
- Verify tooth-specific application.  
**Notes:**  
- Not for free grafts (see D4277).  
- Narrative/X-rays justify need.  
- Often for esthetics or recession.  

#### Code: D4273
**Heading:** Autogenous connective tissue graft procedure  
**Description:** Uses autogenous tissue (e.g., palate) grafted to enhance gingival coverage or support.  
**When to Use:**  
- The patient needs gingival augmentation or root coverage with autogenous tissue from a donor site.  
- Use for primary site grafting.  
**What to Check:**  
- Confirm defect and donor site (e.g., palate) via exam.  
- Assess graft size and recipient need.  
- Check if additional sites apply (see D4283).  
- Verify surgical technique.  
**Notes:**  
- Use D4283 for additional sites.  
- Narrative details donor/recipient sites.  
- Not for non-autogenous grafts (see D4275).  

#### Code: D4277
**Heading:** Free soft tissue graft procedure (including surgical sites)  
**Description:** A free graft from a donor site is placed to improve tissue volume/coverage.  
**When to Use:**  
- The patient requires a free soft tissue graft for gingival augmentation or coverage at a surgical site.  
- Use for non-edentulous areas.  
**What to Check:**  
- Confirm defect and donor site via exam.  
- Assess graft purpose (e.g., volume, esthetics).  
- Check if edentulous (use D4278 if so).  
- Verify surgical site condition.  
**Notes:**  
- Includes donor site—don’t code separately.  
- Use D4278 for edentulous areas.  
- Narrative/X-rays support claim.  

#### Code: D4278
**Heading:** Free soft tissue graft procedure (edentulous areas)  
**Description:** A free graft applied to edentulous tooth positions for tissue restoration or prosthetic prep.  
**When to Use:**  
- The patient has an edentulous area needing a free soft tissue graft for tissue integrity or prosthetics.  
- Use for toothless sites.  
**What to Check:**  
- Confirm edentulous site via exam/radiograph.  
- Assess graft need (e.g., ridge augmentation).  
- Check if paired with other codes (e.g., D4260).  
- Verify donor site availability.  
**Notes:**  
- Use D4277 for non-edentulous sites.  
- Narrative links to prosthetic goal.  
- Includes donor site coding.  

#### Code: D4322
**Heading:** Splint — intracoronal  
**Description:** An intracoronal splint stabilizes mobile teeth in periodontal therapy.  
**When to Use:**  
- The patient has mobile teeth needing internal stabilization (e.g., via resin/composite) during periodontal treatment.  
- Use for structural support.  
**What to Check:**  
- Confirm tooth mobility and periodontal status via exam.  
- Assess splint placement (intracoronal).  
- Check if paired with other perio codes.  
- Verify patient bite stability.  
**Notes:**  
- Use D4323 for extracoronal splints.  
- Narrative justifies mobility level.  
- Temporary or permanent—specify intent.  

#### Code: D4345
**Heading:** Scaling in the presence of inflammation  
**Description:** Removes plaque/calculus/stains with moderate to severe gingival inflammation, without invasive procedures.  
**When to Use:**  
- The patient has generalized moderate/severe gingival inflammation needing scaling.  
- Use for non-surgical inflammation reduction.  
**What to Check:**  
- Confirm inflammation level via exam/charting.  
- Assess plaque/calculus presence.  
- Check no SRP (D4341) is performed.  
- Verify full-mouth or localized need.  
**Notes:**  
- Use D4346 for full-mouth scaling.  
- Not with invasive perio surgery.  
- Documentation of inflammation key.  

#### Code: D4355
**Heading:** Full mouth debridement  
**Description:** Removes gross deposits for comprehensive periodontal evaluation/diagnosis.  
**When to Use:**  
- The patient has heavy plaque/calculus preventing a full perio exam, requiring debridement.  
- Use as a preliminary step.  
**What to Check:**  
- Confirm gross deposits via exam/radiograph.  
- Assess inability to chart/evaluate perio status.  
- Check if followed by perio treatment (e.g., D4341).  
- Verify full-mouth application.  
**Notes:**  
- Not for routine prophylaxis (see D1110).  
- Narrative/X-rays justify need.  
- Often a diagnostic precursor.  

#### Code: D4381
**Heading:** Localized delivery of antimicrobial agents  
**Description:** Applies antimicrobial agents into periodontal pockets as an adjunct to scaling/root planing.  
**When to Use:**  
- The patient has specific pockets needing antimicrobial treatment post-scaling.  
- Use for localized infection control.  
**What to Check:**  
- Confirm prior SRP (e.g., D4341) and pocket depths via charting.  
- Assess site-specific infection/inflammation.  
- Check agent type and delivery method.  
- Verify per-site application.  
**Notes:**  
- Adjunct code—pairs with SRP.  
- Narrative specifies sites/agents.  
- Not for full-mouth treatment.  

#### Code: D4283
**Heading:** Autogenous connective tissue graft (additional site)  
**Description:** Extends D4273 for additional sites needing autogenous tissue grafting.  
**When to Use:**  
- The patient has additional sites beyond D4273 needing autogenous grafts for gingival enhancement.  
- Use per extra site.  
**What to Check:**  
- Confirm D4273 is used and additional sites exist via exam.  
- Assess graft need and donor site capacity.  
- Check site-specific application.  
- Verify autogenous source.  
**Notes:**  
- Not standalone—requires D4273.  
- Specify site count in documentation.  
- Narrative/X-rays support claim.  

#### Code: D4275
**Heading:** Non-autogenous connective tissue graft  
**Description:** Uses non-autogenous tissue (e.g., allograft) for gingival grafting.  
**When to Use:**  
- The patient needs gingival augmentation with non-autogenous tissue at a primary site.  
- Use when avoiding donor site harvest.  
**What to Check:**  
- Confirm defect and graft need via exam.  
- Assess non-autogenous material type.  
- Check if additional sites apply (see D4285).  
- Verify surgical site condition.  
**Notes:**  
- Use D4285 for additional sites.  
- Narrative specifies material source.  
- Not for autogenous grafts (see D4273).  

#### Code: D4285
**Heading:** Non-autogenous connective tissue graft (additional site)  
**Description:** Extends D4275 for additional sites needing non-autogenous tissue grafting.  
**When to Use:**  
- The patient has additional sites beyond D4275 needing non-autogenous grafts.  
- Use per extra site.  
**What to Check:**  
- Confirm D4275 is used and additional sites exist via exam.  
- Assess graft need and material availability.  
- Check site-specific application.  
- Verify non-autogenous source.  
**Notes:**  
- Not standalone—requires D4275.  
- Specify site count in documentation.  
- Narrative/X-rays justify need.  

#### Code: D4274
**Heading:** Mesial/distal wedge procedure  
**Description:** Removes a tissue wedge mesial/distal to a tooth to eliminate pockets or aid restorative access.  
**When to Use:**  
- The patient has a periodontal pocket or tissue excess mesial/distal to a tooth needing surgical removal.  
- Use for localized defect correction.  
**What to Check:**  
- Confirm pocket/defect location via charting/radiograph.  
- Assess wedge necessity (e.g., pocket depth).  
- Check if restorative access is a factor.  
- Verify tooth-specific application.  
**Notes:**  
- Per-tooth code—document site.  
- Narrative links to perio/restorative goal.  
- Not for quadrant-wide surgery.  

#### Code: D4276
**Heading:** Combined connective tissue and pedicle graft  
**Description:** Combines connective tissue grafting and a pedicle flap for periodontal repair/augmentation.  
**When to Use:**  
- The patient needs both a connective tissue graft and pedicle flap for enhanced gingival repair at a site.  
- Use for complex defects.  
**What to Check:**  
- Confirm defect and dual-technique need via exam.  
- Assess donor site and pedicle feasibility.  
- Check esthetic/functional goals.  
- Verify site-specific application.  
**Notes:**  
- Combines D4270/D4273 elements—don’t code separately.  
- Narrative/X-rays justify complexity.  
- Often for severe recession.  

#### Code: D4323
**Heading:** Splint — extracoronal  
**Description:** An extracoronal splint stabilizes mobile teeth externally in periodontal therapy.  
**When to Use:**  
- The patient has mobile teeth needing external stabilization (e.g., wire/resin) during periodontal treatment.  
- Use for structural support.  
**What to Check:**  
- Confirm mobility and perio status via exam.  
- Assess splint placement (extracoronal).  
- Check if paired with other codes.  
- Verify bite stability post-splinting.  
**Notes:**  
- Use D4322 for intracoronal splints.  
- Narrative justifies mobility level.  
- Specify temporary/permanent intent.  

#### Code: D4341
**Heading:** Periodontal scaling and root planing (four or more teeth per quadrant)  
**Description:** Non-surgical scaling/root planing of ≥4 teeth per quadrant to remove plaque/calculus and promote healing.  
**When to Use:**  
- The patient has ≥4 teeth per quadrant with periodontal disease needing SRP.  
- Use for non-surgical perio treatment.  
**What to Check:**  
- Confirm ≥4 teeth and pocket depths via charting.  
- Assess calculus/inflammation presence.  
- Check quadrant-specific application.  
- Verify no flap surgery (see D4240).  
**Notes:**  
- Use D4342 for fewer teeth.  
- Narrative/X-rays document perio status.  
- Not with D4240/D4241 (includes SRP).  

#### Code: D4342
**Heading:** Periodontal scaling and root planing (one to three teeth per quadrant)  
**Description:** Non-surgical scaling/root planing of 1-3 teeth per quadrant for localized perio treatment.  
**When to Use:**  
- The patient has 1-3 teeth per quadrant with perio disease needing SRP.  
- Use for localized non-surgical care.  
**What to Check:**  
- Confirm 1-3 teeth and pocket depths via charting.  
- Assess calculus/inflammation level.  
- Check quadrant-specific application.  
- Verify no flap surgery (see D4241).  
**Notes:**  
- Use D4341 for ≥4 teeth.  
- Documentation of sites critical.  
- Not with D4241 (includes SRP).  

#### Code: D4346
**Heading:** Scaling in presence of moderate to severe inflammation (full mouth)  
**Description:** Full-mouth scaling for moderate/severe gingival inflammation to reduce swelling and promote health.  
**When to Use:**  
- The patient has full-mouth moderate/severe inflammation needing scaling.  
- Use for non-surgical inflammation control.  
**What to Check:**  
- Confirm inflammation level via exam/charting.  
- Assess plaque/calculus presence full-mouth.  
- Check no SRP or surgery is performed.  
- Verify generalized condition.  
**Notes:**  
- Use D4345 for localized scaling.  
- Not with D4341/D4342.  
- Narrative/X-rays justify inflammation.  

#### Code: D4910
**Heading:** Periodontal maintenance  
**Description:** Ongoing maintenance post-active therapy, including plaque/calculus removal and perio monitoring.  
**When to Use:**  
- The patient has completed active perio therapy (e.g., D4341, D4260) and needs ongoing care.  
- Use for long-term perio health.  
**What to Check:**  
- Confirm prior active therapy via records.  
- Assess current perio status via charting.  
- Check plaque/calculus levels.  
- Verify maintenance frequency (e.g., 3-6 months).  
**Notes:**  
- Not for initial treatment—post-therapy only.  
- Narrative links to prior treatment.  
- Replaces prophylaxis (D1110) in perio patients.  

#### Code: D4920
**Heading:** Unscheduled dressing change  
**Description:** Unscheduled change of periodontal dressings to manage healing/complications post-surgery.  
**When to Check:**  
- Confirm prior perio surgery and dressing use via records.  
- Assess need for change (e.g., irritation, loss).  
- Check timing (unscheduled, not routine).  
- Verify dentist-performed change.  
**Notes:**  
- Per-visit code—document reason.  
- Narrative explains urgency.  
- Not for scheduled follow-ups.  

#### Code: D4921
**Heading:** Gingival irrigation per quadrant  
**Description:** Irrigation of gingival tissues in a quadrant to remove debris or deliver therapeutic agents.  
**When to Use:**  
- The patient needs quadrant-specific gingival irrigation as part of perio treatment.  
- Use for adjunctive care.  
**What to Check:**  
- Confirm perio condition and irrigation need via exam.  
- Assess agent used (e.g., antimicrobial).  
- Check quadrant-specific application.  
- Verify not full-mouth (see D4346).  
**Notes:**  
- Adjunct code—pairs with other treatments.  
- Narrative specifies agent/purpose.  
- Not for routine cleaning.  

#### Code: D4999
**Heading:** Unspecified periodontal procedure  
**Description:** Used for a procedure not adequately described by a code. Describe the procedure.  
**When to Use:**  
- The patient undergoes a unique perio procedure not covered by specific codes (e.g., experimental technique).  
- Use with a detailed report.  
**What to Check:**  
- Confirm no standard code applies via procedure review.  
- Assess procedure purpose and outcome.  
- Check diagnostic support (e.g., X-rays).  
- Verify patient consent for non-standard care.  
**Notes:**  
- Requires detailed narrative (time, materials).  
- Insurance may delay payment—submit evidence.  
- Use sparingly—specific codes preferred.  

---

### Key Takeaways:
- **Tooth Count Matters:** Codes split by 1-3 vs. ≥4 teeth per quadrant—count accurately.  
- **Surgical vs. Non-Surgical:** Distinguish procedures (e.g., D4341 vs. D4240) by scope, not effort.  
- **Adjunctive Coding:** Grafts, barriers, and maintenance often pair with primary codes—don’t bundle.  
- **Healthy vs. Diseased:** Some codes (e.g., D4249) require healthy periodontium—verify status.  
- **Documentation Critical:** Insurance demands perio charting, X-rays, and narratives for surgical/post-op codes.




Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_surgical_services_code(scenario, temperature=0.0):
    """
    Extract surgical periodontal services code(s) for a given scenario.
    """
    try:
        chain = create_surgical_services_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Surgical periodontal services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_surgical_services_code: {str(e)}")
        return ""

def activate_surgical_services(scenario):
    """
    Activate surgical periodontal services analysis and return results.
    """
    try:
        return extract_surgical_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_surgical_services: {str(e)}")
        return "" 