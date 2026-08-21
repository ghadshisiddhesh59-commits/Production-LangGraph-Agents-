from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.agent.tools import TOOLS
from backend.config import (
    LLM_PROVIDER,
    LLM_MODEL,
    OLLAMA_BASE_URL,
    GEMINI_API_KEY,
    LLM_TEMPERATURE,
    MAX_RETRIES,
    LLM_TIMEOUT
)
from backend.logger import logger


class Agent:

    def __init__(self):

        logger.info("Initializing AI Agent")

        if LLM_PROVIDER == "ollama":

            self.llm = ChatOllama(
                model=LLM_MODEL,
                base_url=OLLAMA_BASE_URL,
                temperature=LLM_TEMPERATURE
            )

        elif LLM_PROVIDER == "gemini":

            self.llm = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                google_api_key=GEMINI_API_KEY,
                temperature=LLM_TEMPERATURE,
                max_retries=MAX_RETRIES,
                timeout=LLM_TIMEOUT
            )

        else:

            raise ValueError(
                f"Unsupported LLM provider: {LLM_PROVIDER}"
            )

        self.tools = TOOLS

        self.llm_with_tools = self.llm.bind_tools(
            self.tools
        )

        logger.info(
            "Agent initialized with provider=%s, model=%s",
            LLM_PROVIDER,
            LLM_MODEL
        )

    def run(self, messages):

        logger.info("Agent processing request")

        try:

            response = self.llm_with_tools.invoke(
                messages
            )

            logger.info("Agent response generated")

            return response

        except Exception:

            logger.exception(
                "Agent execution failed"
            )

            raise

    def stream(self, messages):

        return self.llm_with_tools.stream(
            messages
        )