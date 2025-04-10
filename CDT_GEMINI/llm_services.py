import os
import time
import logging
from typing import Dict, Any, Union
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Gemini configuration from environment
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.0"))

# Initialize Gemini for direct API calls
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class LLMService:
    def __init__(self, temperature=GEMINI_TEMPERATURE, max_retries=3, 
                 retry_delay=2, gemini_model=GEMINI_MODEL):
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.gemini_model = gemini_model
        
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found in environment variables")
        
        self._initialize_model()
    
    def set_model(self, model_name):
        if model_name and model_name != self.gemini_model:
            self.gemini_model = model_name
            logger.info(f"Updating model to: {model_name}")
            self._initialize_model()
            return True
        return False
    
    def set_temperature(self, temperature):
        if temperature is not None and temperature != self.temperature:
            self.temperature = temperature
            logger.info(f"Updating temperature to: {temperature}")
            self._initialize_model()
            return True
        return False
    
    def _initialize_model(self):
        try:
            self.gemini_llm = ChatGoogleGenerativeAI(
                model=self.gemini_model,
                temperature=self.temperature,
                google_api_key=GEMINI_API_KEY
            )
            logger.info(f"Model: {self.gemini_model} (temp: {self.temperature})")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise ValueError(f"Failed to initialize model: {e}")
    
    def create_chain(self, prompt_template):
        # Convert string to PromptTemplate if needed
        if isinstance(prompt_template, str):
            import re
            variables = list(set(re.findall(r'\{([^{}]*)\}', prompt_template)))
            prompt_template = PromptTemplate(
                template=prompt_template,
                input_variables=variables
            )
        return LLMChain(llm=self.gemini_llm, prompt=prompt_template)
    
    def generate_response(self, prompt):
        for attempt in range(self.max_retries + 1):
            try:
                response = self.gemini_llm.invoke([HumanMessage(content=prompt)])
                return response.content.strip()
            except Exception as e:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed after {self.max_retries} attempts: {e}")
    
    def invoke_chain(self, chain, inputs):
        for attempt in range(self.max_retries + 1):
            try:
                return chain.invoke(inputs)
            except Exception as e:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Chain invocation failed after {self.max_retries} attempts: {e}")

# Singleton instance
llm_service = LLMService()

# Public API functions
def get_llm_service():
    return llm_service

def set_model_for_file(model_name):
    return llm_service.set_model(model_name)

def set_temperature_for_file(temperature):
    return llm_service.set_temperature(temperature)

def create_chain(prompt_template):
    return llm_service.create_chain(prompt_template)

def generate_response(prompt):
    return llm_service.generate_response(prompt)

def invoke_chain(chain, inputs):
    return llm_service.invoke_chain(chain, inputs) 