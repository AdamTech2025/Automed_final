"""
Module containing the standardized ICD prompt template.
"""

PROMPT = """Based on the scenario, identify ONLY the accurate ICD-10 code.

Instructions:
1. Carefully analyze the scenario focusing on the primary condition or finding.
2. Select relevant ICD-10 code that best represents the scenario.

Return your answer in this exact format:
CODE: [specific ICD-10 code or codes, separated by comma, or none if no code is applicable]
EXPLANATION: [provide a brief, concise explanation of why this code(s) is (are) the most appropriate]
DOUBT: [list any uncertainty about the selected code(s)]""" 