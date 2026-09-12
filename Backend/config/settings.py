import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-120b"
)

MAX_DEBUG_ITERATIONS = int(
    os.getenv(
        "MAX_DEBUG_ITERATIONS",
        "3"
    )
)