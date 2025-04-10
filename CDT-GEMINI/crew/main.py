import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Task, Agent, Crew
from sqlalchemy import create_engine

### 🏥 Step 1: Database Connection & Data Loading ###
db_path = "C:/surya/Muscle Mind/RCM/Medical Dental Gpt/Medical-coding-dental/med_gpt.sqlite3"

def load_data():
    """Loads the most recent record from the dental_analysis table."""
    engine = create_engine(f"sqlite:///{db_path}")
    query = "SELECT * FROM dental_analysis ORDER BY create_at DESC LIMIT 1"
    data = pd.read_sql_query(query, con=engine)
    engine.dispose()
    if data.empty:
        raise ValueError("No records found in dental_analysis table.")
    return data

### 🔬 Step 2: OpenAI o1-mini Model Setup ###
openai_api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=openai_api_key,
    temperature=0.2,
    max_tokens=2000
)

### 🧠 Step 3: Define AI Agents ###
data_loader_agent = Agent(
    role="Data Loader",
    goal="Retrieve the most recent dental analysis record for processing.",
    backstory="Specialist in fetching and preparing the latest medical data efficiently.",
    verbose=True,
    allow_delegation=False
)

analyzer_agent = Agent(
    role="Medical Data Analyst",
    goal="Analyze the latest patient question and processed data for insights.",
    backstory="Expert in interpreting dental records and coding contexts.",
    llm=llm,
    verbose=True
)

auditor_agent = Agent(
    role="Medical Coding Auditor",
    goal="Audit CDT and ICD codes in the latest record for accuracy.",
    backstory="Specialist in dental coding standards and compliance.",
    llm=llm,
    verbose=True
)

verifier_agent = Agent(
    role="Verification Specialist",
    goal="Cross-verify CDT and ICD doubts and decide if user clarification is needed.",
    backstory="Authority on coding compliance with decision-making capabilities.",
    llm=llm,
    verbose=True
)

### 🔄 Step 4: Define Tasks for Agents ###
task_load_data = Task(
    description="Extract the most recent record from the dental_analysis table.",
    expected_output="A DataFrame with the latest dental analysis data.",
    agent=data_loader_agent,
    function=load_data
)

task_analyze_data = Task(
    description=(
        "Analyze the 'user_question' and 'processed_clean_data' from the latest record. "
        "Provide insights on the patient scenario and relevance to CDT and ICD coding."
    ),
    expected_output="A detailed report on the patient scenario and coding trends.",
    agent=analyzer_agent,
    context=[task_load_data]
)

task_audit_codes = Task(
    description=(
        "Audit the 'final_cdt_code' and 'final_icd_code' in the latest record. "
        "Check consistency with 'cdt_topic_range', 'cdt_subtopic_range', 'icd_topic_name', "
        "and their respective explanations."
    ),
    expected_output="A report on code accuracy and any flagged inconsistencies.",
    agent=auditor_agent,
    context=[task_load_data]
)

task_verify_compliance = Task(
    description=(
        "Verify that 'final_cdt_code' and 'final_icd_code' comply with dental and medical standards. "
        "Analyze 'cdt_topic_doubt' and 'icd_topic_doubt' fields critically. "
        "Determine if the doubts are valid and relevant to coding or compliance (e.g., could affect billing or accuracy). "
        "If a doubt is valid and requires clarification, decide to ask the user a specific question based on its content. "
        "If the doubt is trivial, irrelevant, or already addressed in the record, do not prompt the user."
    ),
    expected_output=(
        "A compliance report detailing code accuracy and doubt analysis. "
        "Include a decision: either 'No clarification needed' or 'Ask the user: [specific question]'."
    ),
    agent=verifier_agent,
    context=[task_load_data, task_analyze_data, task_audit_codes]
)

### 🎯 Step 5: Assemble the Crew ###
crew = Crew(
    agents=[data_loader_agent, analyzer_agent, auditor_agent, verifier_agent],
    tasks=[task_load_data, task_analyze_data, task_audit_codes, task_verify_compliance],
    verbose=True,
    process="sequential"
)

### 🚀 Step 6: Execute the Crew ###
def main():
    try:
        print("Starting dental analysis crew...")
        result = crew.kickoff()

        # Display the latest record
        latest_data = load_data()
        print("\nLatest Record:\n", latest_data.to_string(index=False))

        # Handle CrewOutput based on its actual structure
        print("\nFinal Report:")
        if hasattr(result, 'tasks'):  # For older versions or if tasks attribute exists
            for task in result.tasks:
                print(f"\n{task.agent.role} Output:")
                print(task.output)
            verifier_output = result.tasks[-1].output
        else:  # For newer versions where result might be a string or dict
            print(f"Raw Crew Output: {result}")
            # Assuming verifier's output is the last part of a string or a specific key
            # Adjust based on actual output format after inspection
            verifier_output = str(result)  # Fallback to string conversion

        # Handle verifier's decision on doubts
        if isinstance(verifier_output, str) and "ask the user" in verifier_output.lower():
            question_start = verifier_output.lower().find("ask the user:") + len("ask the user:")
            question = verifier_output[question_start:].strip() if question_start > len("ask the user:") else "Please clarify the doubts noted."
            response = input(f"\nVerifier's Question: {question} ").strip()
            print(f"User Response: {response}")
            # Optional: Update database with response
            # update_database(latest_data['id'].iloc[0], response)
        
        else:
            print("\nNo clarification needed based on verifier's analysis.")

        # Display final validated codes
        print("\nValidated Codes:")
        print(f"Final CDT Code: {latest_data['final_cdt_code'].iloc[0]}")
        print(f"Final ICD Code: {latest_data['final_icd_code'].iloc[0]}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()