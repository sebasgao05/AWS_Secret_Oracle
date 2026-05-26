"""Cliente de NVIDIA API (Gemma) como modelo de respaldo."""

import requests

from src.config import NVIDIA_API_KEY, NVIDIA_API_URL, NVIDIA_MODEL_ID


def invoke_with_image(image_base64: str, media_type: str, prompt: str, max_tokens: int = 150) -> str:
    """Invoca Gemma con una imagen y un prompt de texto.

    Args:
        image_base64: Imagen codificada en base64.
        media_type: Tipo MIME de la imagen (e.g. image/jpeg).
        prompt: Texto del prompt.
        max_tokens: Máximo de tokens en la respuesta.

    Returns:
        Texto de la respuesta del modelo.
    """
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json",
    }

    image_url_data = f"data:{media_type};base64,{image_base64}"

    payload = {
        "model": NVIDIA_MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url_data},
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.20,
        "top_p": 0.70,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": False,
    }

    response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
