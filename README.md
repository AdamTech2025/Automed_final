# Automed - AI-Powered Medical Coding Assistant

## Overview

Automed is a comprehensive web application designed to assist medical professionals, particularly in the dental field, with accurate clinical scenario analysis and medical code suggestion (CDT and ICD codes). It leverages Large Language Models (LLMs) via OpenRouter to understand clinical narratives, classify relevant medical topics, ask clarifying questions, inspect the scenario against coding guidelines, and suggest appropriate codes.

The project consists of two main parts:
1.  **Backend (`CDT_GEMINI`):** A Python-based API built with FastAPI, handling the core logic, LLM interactions, database operations (using Supabase), and user authentication.
2.  **Frontend (`Frontend_boilerplate_react`):** A React-based user interface built with Vite and styled using Tailwind CSS, providing a user-friendly way to interact with the backend API.

## Features

*   **Clinical Scenario Input:** Users can input dental clinical scenarios in natural language.
*   **Scenario Cleaning & Standardization:** The backend processes the input, cleaning and standardizing the text for better analysis.
*   **CDT & ICD Code Classification:** Identifies potential CDT (Current Dental Terminology) and ICD (International Classification of Diseases) code categories relevant to the scenario.
*   **Topic Activation:** Dynamically activates specific topic modules based on the classified code ranges/categories.
*   **Intelligent Questioning:** (Questioner Module) Asks clarifying questions to the user if the initial scenario lacks necessary details for accurate coding.
*   **Code Inspection:** (Inspector Module) Analyzes the scenario against specific CDT/ICD coding rules and guidelines to validate potential codes.
*   **Code Suggestion:** Provides suggested CDT and ICD codes based on the comprehensive analysis.
*   **Custom Code Analysis:** Allows users to input a specific code and analyze its applicability to the scenario.
*   **User Authentication:** Secure user registration and login system.
*   **User Activity Tracking:** Stores analysis history for registered users.
*   **Admin Dashboard:** Provides administrators with an overview of all user activity (requires admin role).
*   **Responsive UI:** Frontend built with React and Tailwind CSS for a modern user experience.

## Tech Stack

**Backend (`CDT_GEMINI`)**
*   **Framework:** FastAPI
*   **Language:** Python 3.x
*   **LLM Interaction:** OpenRouter API (interfacing with models like Google Gemini), Langchain
*   **Database:** Supabase (PostgreSQL)
*   **Authentication:** Supabase Auth, JWT (via `python-jose`, `passlib`, `bcrypt`)
*   **Core Libraries:** `uvicorn`, `pydantic`, `sqlalchemy` (likely for ORM patterns, though Supabase client is primary), `python-dotenv`
*   **Deployment:** (Inferred from `runtime.txt`) Likely targeting a platform that uses this file (e.g., Heroku, PythonAnywhere).

**Frontend (`Frontend_boilerplate_react`)**
*   **Framework:** React 18
*   **Build Tool:** Vite
*   **Language:** JavaScript (JSX)
*   **Styling:** Tailwind CSS, Styled Components
*   **Routing:** React Router DOM
*   **State Management:** (Implicit) React Context API or component state (No dedicated library like Redux/Zustand listed in main dependencies)
*   **API Communication:** Axios
*   **UI Components/Libraries:** Ant Design (`antd`), FontAwesome, React Icons, React Slick (Carousel), React Toastify (Notifications), AOS (Scroll Animations), React Vertical Timeline
*   **Form Handling:** React Hook Form
*   **Linting:** ESLint

## Project Structure

```
.
├── CDT_GEMINI/             # Backend FastAPI Application
│   ├── add_codes/          # Module for analyzing custom codes
│   ├── auth/               # Authentication logic and routes
│   ├── icdtopics/          # Specific ICD topic activation modules
│   ├── subtopics/          # Shared subtopic logic/parsing (likely)
│   ├── templates/          # HTML Templates (if any used by FastAPI)
│   ├── topics/             # Specific CDT topic activation modules
│   ├── .venv/              # Virtual environment
│   ├── __pycache__/
│   ├── app.py              # Main FastAPI application file
│   ├── cdt_classifier.py   # Classifier for CDT codes
│   ├── database.py         # Supabase database interaction logic
│   ├── data_cleaner.py     # Scenario cleaning/processing logic
│   ├── icd_classifier.py   # Classifier for ICD codes
│   ├── icd_inspector.py    # Inspector logic for ICD codes
│   ├── inspector.py        # Inspector logic for CDT codes
│   ├── llm_services.py     # LLM interaction service (OpenRouter)
│   ├── questioner.py       # Logic for asking clarifying questions
│   ├── sub_topic_registry.py # Registry for topic activation functions
│   ├── subtopic.py         # Subtopic parsing/management logic
│   ├── requirements.txt    # Python dependencies
│   ├── runtime.txt         # Python runtime version for deployment
│   └── ...
├── Frontend_boilerplate_react/ # Frontend React Application
│   ├── public/             # Static assets
│   ├── src/                # React source code (components, pages, etc.)
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Application pages/views
│   │   ├── App.jsx         # Main application component
│   │   └── main.jsx        # Entry point for React app
│   ├── data/               # Placeholder for frontend data?
│   ├── node_modules/       # Node.js dependencies
│   ├── index.html          # Main HTML entry point for Vite
│   ├── package.json        # Node.js dependencies and scripts
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   ├── vite.config.js      # Vite configuration (including proxy)
│   └── ...
└── README.md               # This file
```

## Setup and Installation

**Prerequisites:**
*   Python 3.x and `pip`
*   Node.js and `npm` (or `yarn`)
*   Access to a Supabase project (URL and Key)
*   OpenRouter API Key

**Backend (`CDT_GEMINI`)**
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Automed_final # Or your project root directory
    ```
2.  **Navigate to the backend directory:**
    ```bash
    cd CDT_GEMINI
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure environment variables:** Create a `.env` file in the `CDT_GEMINI` directory and add the following:
    ```dotenv
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_anon_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    # Optional: Specify a different OpenRouter model
    # OPENROUTER_MODEL=google/gemini-pro
    # Optional: Set JWT Secret and Algorithm for auth
    JWT_SECRET=your_strong_jwt_secret
    ALGORITHM=HS256
    # Optional: Frontend URL for CORS
    FRONTEND_URL=http://localhost:5173
    ```
6.  **Run the backend server:**
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://localhost:8000`.

**Frontend (`Frontend_boilerplate_react`)**
1.  **Navigate to the frontend directory:**
    ```bash
    cd ../Frontend_boilerplate_react # From CDT_GEMINI directory
    # Or cd Frontend_boilerplate_react from the root
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
3.  **Run the frontend development server:**
    ```bash
    npm run dev
    # or yarn dev
    ```
    The frontend application will be available at `http://localhost:5173` (or another port if 5173 is busy). The `vite.config.js` includes a proxy to automatically forward `/api` requests to the backend running on `http://localhost:8000`.

## Usage

1.  Ensure both the backend and frontend servers are running.
2.  Open your web browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
3.  Register or log in if authentication is required for the features you want to use.
4.  Enter a clinical scenario into the provided input area.
5.  Submit the scenario for analysis.
6.  The application will guide you through the steps: cleaning, classification, potential questions, inspection, and code suggestions.
7.  Interact with the interface to provide more information (if asked) or review the suggested codes.
8.  Use the custom code analysis feature to check the relevance of specific codes.

## Backend API Endpoints (Partial List)

*   `/auth/...`: Authentication routes (login, register, verify).
*   `POST /api/analyze`: Main endpoint to submit a scenario for full analysis.
*   `POST /api/add-custom-code`: Analyzes a user-provided code against the scenario.
*   `POST /api/store-code-status`: Stores user feedback on suggested/rejected codes.
*   `GET /api/user/activity`: Retrieves the current user's analysis history.
*   `GET /api/admin/all-users`: (Admin only) Retrieves activity for all users.
*   `GET /`: Root endpoint (simple health check).

*(Refer to `CDT_GEMINI/app.py` for a complete list and request/response models)*

## Contributing

[Optional: Add guidelines for contributing if this is an open project.]

## License

[Optional: Specify the project license, e.g., MIT, Apache 2.0.] 