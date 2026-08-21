from langchain_ollama import ChatOllama

from backend.agent.tools import TOOLS
from backend.config import(
    LLM_MODEL,
    OLLAMA_BASE_URL,
    LLM_TEMPERATURE
)
from backend.logger import logger

class Agent:

    def __init__(self):

        logger.info("Initializing AI Agent")

        self.llm = ChatOllama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=LLM_TEMPERATURE
        )

        self.tools = TOOLS
        

        self.llm_with_tools = self.llm.bind_tools(
            self.tools
        )

        logger.info(
            "Agent initialized with model: %s",
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
        
        