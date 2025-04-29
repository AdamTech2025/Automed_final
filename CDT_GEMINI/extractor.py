import os
import io
import json
import re
import base64
import time
from typing import Dict, Any, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from werkzeug.utils import secure_filename
import PyPDF2
from dotenv import load_dotenv
import openai
import requests
import logging
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Basic Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Dental Scenario Extractor API",
    description="API for extracting and processing dental scenarios from various file formats",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration ---
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-pro-preview-03-25")
OPENROUTER_TEMPERATURE = float(os.getenv("OPENROUTER_TEMPERATURE", "0.0"))
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:5000")
OPENROUTER_SITE_NAME = os.getenv("OPENROUTER_SITE_NAME", "Scenario Splitter API")
DEFAULT_TEMP = 0.0

class LLMService:
    def __init__(self, temperature=DEFAULT_TEMP, max_retries=3, 
                 retry_delay=2, model=OPENROUTER_MODEL):
        if not OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API key not found in environment variables")
        
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.model = model
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            self.client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": OPENROUTER_SITE_URL,
                    "X-Title": OPENROUTER_SITE_NAME
                }
            )
            logger.info(f"Initialized OpenRouter with model: {self.model} (temp: {self.temperature})")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter: {e}")
            raise ValueError(f"Failed to initialize client: {e}")
    
    def set_model(self, model_name: str):
        if model_name and model_name != self.model:
            self.model = model_name
            logger.info(f"Updated model to: {model_name}")
            return True
        return False
    
    def set_temperature(self, temperature: float):
        if temperature is not None and temperature != self.temperature:
            self.temperature = temperature
            logger.info(f"Updated temperature to: {temperature}")
            return True
        return False
    
    def generate_response(self, prompt: Union[str, Dict], image_url: str = None):
        for attempt in range(self.max_retries + 1):
            try:
                messages = []
                if isinstance(prompt, str):
                    content = [{"type": "text", "text": prompt}]
                    if image_url:
                        content.append({
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        })
                    messages.append({"role": "user", "content": content})
                elif isinstance(prompt, dict):
                    messages.append(prompt)
                elif isinstance(prompt, list):
                    messages = prompt
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt < self.max_retries:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed after {self.max_retries} attempts: {e}")

# Initialize LLM service
llm_service = LLMService()

# Initialize upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logging.info(f"Created upload folder: {UPLOAD_FOLDER}")

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'mp3', 'wav'}
MAX_CHAR_LIMIT = 750000 # Increased limit significantly, but monitor API costs/limits

# --- Logging API Key Status ---
if not openai.api_key:
    logging.warning("OpenAI API key not found. Image and audio processing will be disabled.")
else:
    logging.info("OpenAI API key loaded.")

if not OPENROUTER_API_KEY:
    logging.warning("OpenRouter API key (OPENROUTER_API_KEY) not found. AI-based scenario splitting will be disabled.")
else:
    logging.info(f"OpenRouter API key loaded. Using model: {OPENROUTER_MODEL}")

# --- Helper Functions ---

def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_char_limit(text):
    """Checks if the extracted text exceeds the character limit."""
    char_count = len(text)
    logging.info(f"Character count check: {char_count} characters.")
    if char_count > MAX_CHAR_LIMIT:
        logging.error(f"Character limit exceeded: {char_count}/{MAX_CHAR_LIMIT}")
        # Consider chunking logic here if needed for very large files,
        # but for now, we raise an error as implemented.
        raise ValueError(f"File content exceeds maximum character limit ({char_count}/{MAX_CHAR_LIMIT} characters)")

# --- Text Extraction Functions (with logging) ---

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file given its path."""
    logging.info(f"Attempting PDF text extraction from: {file_path}")
    text = ""
    try:
        with open(file_path, 'rb') as file_stream:
            pdf_reader = PyPDF2.PdfReader(file_stream)
            num_pages = len(pdf_reader.pages)
            logging.info(f"PDF has {num_pages} pages.")
            for i, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    # else: # Optional: Log pages with no text
                    #     logging.debug(f"No text extracted from PDF page {i+1}")
                except Exception as page_err:
                    logging.warning(f"Could not extract text from PDF page {i+1}: {page_err}")
        extracted_text = text.strip()
        logging.info(f"Successfully extracted {len(extracted_text)} characters from PDF.")
        return extracted_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF ({file_path}): {e}", exc_info=True)
        raise IOError(f"Error processing PDF file: {str(e)}") from e

def extract_text_from_image(file_path):
    """Extracts text from an image file using OpenAI GPT-4o."""
    logging.info(f"Attempting Image text extraction using OpenAI from: {file_path}")
    if not openai.api_key:
        logging.error("OpenAI API key missing for image extraction.")
        raise ValueError("Image text extraction requires an OpenAI API key.")
    try:
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        logging.info("Calling OpenAI GPT-4o API for image text extraction...")
        # Determine image type for data URI (basic check)
        mime_type = f"image/{file_path.rsplit('.', 1)[1].lower()}"
        if mime_type not in ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"]:
             mime_type = "image/jpeg" # Default fallback

        response = openai.chat.completions.create(
            model="gpt-4o", # Use gpt-4o
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text content verbatim from this image. Preserve original line breaks and formatting as accurately as possible. Return only the extracted text."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000 # Allow ample tokens
        )
        extracted_text = response.choices[0].message.content
        logging.info(f"Successfully extracted {len(extracted_text)} characters from image via OpenAI.")
        return extracted_text if extracted_text else ""
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error during image extraction: {e}", exc_info=True)
        raise ConnectionError(f"OpenAI API error (Image): {str(e)}") from e
    except Exception as e:
        logging.error(f"Error extracting text from image ({file_path}): {e}", exc_info=True)
        raise IOError(f"Error processing image file: {str(e)}") from e

def extract_text_from_audio(file_path):
    """Transcribes text from an audio file using OpenAI Whisper."""
    logging.info(f"Attempting Audio transcription using OpenAI Whisper from: {file_path}")
    if not openai.api_key:
        logging.error("OpenAI API key missing for audio transcription.")
        raise ValueError("Audio transcription requires an OpenAI API key.")
    try:
        with open(file_path, "rb") as audio_file:
            logging.info("Calling OpenAI Whisper API for audio transcription...")
            # Check file size (Whisper has a 25MB limit)
            file_size = os.path.getsize(file_path)
            if file_size > 25 * 1024 * 1024:
                 logging.error(f"Audio file size {file_size / (1024*1024):.2f} MB exceeds 25MB limit.")
                 raise ValueError("Audio file exceeds 25MB size limit for Whisper.")

            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        extracted_text = response.text
        logging.info(f"Successfully transcribed {len(extracted_text)} characters from audio via OpenAI.")
        return extracted_text if extracted_text else ""
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error during audio transcription: {e}", exc_info=True)
        raise ConnectionError(f"OpenAI API error (Audio): {str(e)}") from e
    except Exception as e:
        logging.error(f"Error extracting text from audio ({file_path}): {e}", exc_info=True)
        raise IOError(f"Error processing audio file: {str(e)}") from e

def extract_text_from_txt(file_path):
    """Reads text from a TXT file."""
    logging.info(f"Attempting TXT file read from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        logging.info(f"Successfully read {len(text)} characters from TXT file.")
        return text
    except Exception as e:
        logging.error(f"Error reading text file ({file_path}): {e}", exc_info=True)
        raise IOError(f"Error reading text file: {str(e)}") from e

def extract_json_from_text(text):
    """Try to extract a JSON object with a 'scenarios' key from a string."""
    match = re.search(r'\{\s*"scenarios"\s*:\s*\[.*?\]\s*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None

# --- AI Scenario Splitting Logic (Gemini Focused) ---

def split_into_scenarios(text):
    """
    Uses LLMService to split text into distinct scenarios/questions.
    """
    logging.info("Starting AI-driven scenario splitting process...")
    if not text or not isinstance(text, str) or not text.strip():
        logging.warning("Input text is empty or invalid for splitting.")
        return []

    cleaned_text = text.strip()
    min_scenario_length = 50 # Minimum length for a valid scenario chunk

    if not OPENROUTER_API_KEY:
        logging.error("Cannot split scenarios: OpenRouter API Key is not configured.")
        return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []

    logging.info(f"Processing text block of {len(cleaned_text)} characters via OpenRouter ({OPENROUTER_MODEL})...")

    try:
        # Stronger system prompt for scenario splitting
        system_prompt = {
            "role": "system",
            "content": (
                "You are a scenario splitter. Your job is to split the input text into distinct scenarios/questions. "
                "Each scenario/question MUST be a separate string in the output array. "
                "If you do not split, your output will be considered invalid.\n\n"
                "Example input:\n"
                "Scenario 1: ...\\nHow would you code this?\\nScenario 2: ...\\nHow would you code this?\n\n"
                "Example output:\n"
                '{"scenarios": ['
                '"Scenario 1: ...\\nHow would you code this?",'
                '"Scenario 2: ...\\nHow would you code this?"'
                ']}\n\n'
                "Your output MUST be a JSON object with a key 'scenarios' whose value is a JSON array. Each array element MUST be a single scenario/question as a string. If you return only one string, your output will be considered invalid. If you see multiple scenarios/questions, split them into separate array elements. Do not add any commentary or explanation outside the JSON object."
            )
        }

        # User prompt with the actual text
        user_prompt = {
            "role": "user",
            "content": cleaned_text
        }

        # Use LLMService to generate response
        content_string = llm_service.generate_response([system_prompt, user_prompt])

        if not content_string:
            logging.warning("AI response content was empty.")
            return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []

        # Try direct JSON parse first
        try:
            result = json.loads(content_string)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            result = extract_json_from_text(content_string)
        except Exception as parse_err:
            logging.error(f"Error processing AI response structure: {parse_err}. Returning original text as fallback.", exc_info=True)
            return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []

        if result and isinstance(result, dict) and 'scenarios' in result and isinstance(result['scenarios'], list):
            extracted_scenarios = [str(s).strip() for s in result['scenarios'] if isinstance(s, str) and str(s).strip()]
            # --- POST-PROCESSING: If only one scenario, try to split by headings or double newlines ---
            if len(extracted_scenarios) == 1:
                scenario_text = extracted_scenarios[0]
                split_scenarios = re.split(r'(?:\n\s*){2,}|(?=\n[A-Z][^\n]+\n)', scenario_text)
                split_scenarios = [s.strip() for s in split_scenarios if len(s.strip()) >= min_scenario_length]
                if len(split_scenarios) > 1:
                    logging.info(f"Post-processed and split single scenario into {len(split_scenarios)} segments.")
                    return split_scenarios
            final_scenarios = [s for s in extracted_scenarios if len(s) >= min_scenario_length]
            if not final_scenarios and extracted_scenarios:
                logging.warning(f"AI returned scenarios, but all were below min length ({min_scenario_length}). Returning the longest raw AI scenario.")
                return [max(extracted_scenarios, key=len)]
            elif not final_scenarios:
                logging.warning("AI result yielded no valid scenarios after filtering. Returning original text as fallback.")
                return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []
            logging.info(f"AI successfully processed text into {len(final_scenarios)} scenarios.")
            return final_scenarios
        else:
            # Fallback: treat the response as plain text and split
            logging.warning("AI response was not valid JSON. Attempting to split plain text response.")
            text_to_split = content_string.strip()
            split_scenarios = re.split(r'(?:\n\s*){2,}|(?=\n[A-Z][^\n]+\n)', text_to_split)
            split_scenarios = [s.strip() for s in split_scenarios if len(s.strip()) >= min_scenario_length]
            if split_scenarios:
                logging.info(f"Fallback: split plain text into {len(split_scenarios)} scenarios.")
                return split_scenarios
            return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []

    except Exception as ai_err:
        logging.error(f"Unexpected error during AI scenario splitting: {ai_err}. Returning original text as fallback.", exc_info=True)
        return [cleaned_text] if len(cleaned_text) >= min_scenario_length else []

# Export all necessary functions and constants
__all__ = [
    'extract_text_from_txt',
    'extract_text_from_pdf',
    'extract_text_from_image',
    'extract_text_from_audio',
    'allowed_file',
    'check_char_limit',
    'split_into_scenarios',
    'UPLOAD_FOLDER',
    'ALLOWED_EXTENSIONS',
    'MAX_CHAR_LIMIT',
    'llm_service'
]




