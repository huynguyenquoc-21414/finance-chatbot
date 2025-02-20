import os
from dotenv import load_dotenv

load_dotenv()

DEEPINFRA_URL = os.getenv("DEEPINFRA_URL")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
DEEPINFRA_MODEL_VARIANT = os.getenv("DEEPINFRA_MODEL_VARIANT")
