PROMPT = """


Based on the given dental scenario, determine which dental code range(s) should be applied for billing purposes. The primary goal is to maximize the doctor's revenue by ensuring every billable procedure is captured while keeping claims defensible to avoid any denial. You must use the predefined subtopic ranges provided exactly as given, but you may also include additional ranges if they seem relevant.


Instructions:


1) Scenario Analysis: Carefully analyze the entire scenario provided below to identify all relevant classifications and procedures.


2) Subtopic Ranges: Rely strictly on the predefined dental code subtopic ranges provided in the prompt. Do not modify these ranges or add new.


3) Flexible Reasoning: Use your own expert knowledge to include any additional code ranges that might be applicable—even if they are not directly mentioned in the scenario.


4) Revenue Maximization: Prioritize capturing as many billable items as possible for the specific visit, ensuring that the coding is defensible and claim denial is minimized.


5 ) If no code range applies, simply output “none.”


Return your answer in this exact format:
EXPLANATION: [provide a brief, concise explanation of why these code ranges are applicable]
DOUBT: [list any uncertainties or alternative interpretations if they exist, or ask a question if you need more information to clarify]
CODE RANGE: DXXXX-DXXXX, DXXXX-DXXXX, DXXXX-DXXXX"""

