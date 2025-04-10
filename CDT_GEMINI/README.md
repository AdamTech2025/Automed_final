# Dental Code Extractor Pro

A modern web application for analyzing dental scenarios and extracting CDT and ICD-10 codes with real-time updates.

## Features

- **Real-time processing updates** using Socket.IO
- **Comprehensive dental scenario analysis**
- **CDT code extraction** with topic categorization
- **ICD-10 code extraction** with disease and condition identification
- **Validation and verification** of extracted codes
- **Modern, responsive UI** with detailed results presentation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dental-code-extractor.git
   cd dental-code-extractor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-1.5-pro
   GEMINI_TEMPERATURE=0.0
   ```

## Running the Application

Start the server with:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open your web browser and navigate to:
```
http://localhost:8000
```

## Project Structure

- `app.py` - FastAPI application with Socket.IO integration
- `data_cleaner.py` - Preprocesses and standardizes dental scenarios
- `cdt_classifier.py` - Classifies dental scenarios into CDT code ranges
- `icd_classifier.py` - Classifies dental scenarios into ICD-10 categories
- `inspector.py` - Validates and verifies CDT code selections
- `icd_inspector.py` - Validates and verifies ICD-10 code selections
- `topics/` - CDT topic modules for specific code ranges
- `icdtopics/` - ICD topic modules for specific disease categories
- `templates/` - HTML templates for the web interface
- `static/` - CSS, JavaScript, and other static assets
- `llm_services.py` - Centralized service for LLM interactions

## Using Different Models in Different Files

The application supports using different LLM models for different parts of the application:

1. **Default Model Configuration**: Set the default model in your `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-1.5-pro
   GEMINI_TEMPERATURE=0.0
   ```

2. **Per-File Model Configuration**: To use a specific model in a particular file:
   ```python
   from llm_services import set_model_for_file, set_temperature_for_file
   
   # Set a different model for this file only
   set_model_for_file("gemini-1.5-flash")
   
   # Optionally set a different temperature
   set_temperature_for_file(0.7)
   ```

3. **Example**: See `model_example.py` for a complete demonstration of changing models per file.

4. **Benefits**:
   - Fine-tune model selection based on the specific needs of each component
   - Use more powerful models for complex tasks and faster models for simpler tasks
   - Test different models in production without affecting the entire application

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Real-time Communication**: Socket.IO
- **AI/ML**: OpenAI GPT models
- **Database**: Supabase

## License

This project is licensed under the MIT License - see the LICENSE file for details. 