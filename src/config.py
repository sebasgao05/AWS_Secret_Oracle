"""Configuración centralizada del proyecto."""

import os
from dotenv import load_dotenv

load_dotenv()

# AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

# API de imágenes
IMAGE_API_URL = os.getenv(
    "IMAGE_API_URL",
    "https://qqgfg03g58.execute-api.us-east-1.amazonaws.com/prod/random-image",
)

# Bedrock (Claude)
BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-5-haiku-20241022-v1:0"
)

# NVIDIA (Gemma)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_MODEL_ID = os.getenv("NVIDIA_MODEL_ID", "google/gemma-3n-e4b-it")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Juego
MAX_HINTS = 5
