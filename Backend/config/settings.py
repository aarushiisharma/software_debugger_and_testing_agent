import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama3:latest"
)

MAX_DEBUG_ITERATIONS = int(
    os.getenv(
        "MAX_DEBUG_ITERATIONS",
        "3"
    )
)
