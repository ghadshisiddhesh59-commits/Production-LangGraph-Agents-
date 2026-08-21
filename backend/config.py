import os

from dotenv import load_dotenv


load_dotenv()


LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

LLM_TEMPERATURE = float(
    os.getenv(
        "LLM_TEMPERATURE",
        "0"
    )
)

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "2"
    )
)

LLM_TIMEOUT = int(
    os.getenv(
        "LLM_TIMEOUT",
        "60"
    )
)