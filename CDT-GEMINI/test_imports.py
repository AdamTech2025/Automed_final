#!/usr/bin/env python
"""
Test script to verify module imports.
"""
import sys
import os

print("Starting import test...")

try:
    from topics.diagnostics import activate_diagnostic
    print("Successfully imported activate_diagnostic from topics.diagnostics")
except Exception as e:
    print(f"Error importing activate_diagnostic: {e}")

try:
    from subtopics.diagnostics import activate_pre_diagnostic_services
    print("Successfully imported activate_pre_diagnostic_services from subtopics.diagnostics")
except Exception as e:
    print(f"Error importing activate_pre_diagnostic_services: {e}")

try:
    from topics.prosthodonticsremovable import activate_prosthodonticsremovable
    print("Successfully imported activate_prosthodonticsremovable from topics.prosthodonticsremovable")
except Exception as e:
    print(f"Error importing activate_prosthodonticsremovable: {e}")

try:
    from subtopics.Prosthodontics_Removable import activate_repairs_to_partial_dentures
    print("Successfully imported activate_repairs_to_partial_dentures from subtopics.Prosthodontics_Removable")
except Exception as e:
    print(f"Error importing activate_repairs_to_partial_dentures: {e}")

try:
    from topics.prompt import PROMPT
    print("Successfully imported PROMPT from topics.prompt")
except Exception as e:
    print(f"Error importing PROMPT: {e}")

print("Import test completed.") 