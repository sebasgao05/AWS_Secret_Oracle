"""Servicio de validación de respuestas del usuario."""

import json

from src.clients import bedrock, nvidia


def _build_prompt(user_answer: str) -> str:
    """Construye el prompt para validar una respuesta."""
    return f"""Observa esta imagen. El usuario intenta adivinar qué muestra.

La respuesta del usuario es: "{user_answer}"

¿Es correcta o suficientemente cercana? Acepta sinónimos, variaciones, traducciones y descripciones genéricas válidas.
Por ejemplo, si la imagen muestra un "gato persa", acepta "gato", "gatito", "felino", "cat", etc.

Responde SOLO con un JSON así:
{{"correct": true/false, "actual": "nombre correcto de lo que muestra la imagen"}}"""


def validate_answer(
    image_base64: str,
    media_type: str,
    user_answer: str,
    on_fallback=None,
) -> dict:
    """Valida si la respuesta del usuario es correcta.

    Args:
        image_base64: Imagen en base64.
        media_type: Tipo MIME de la imagen.
        user_answer: Respuesta del usuario.
        on_fallback: Callback opcional cuando se usa el modelo de respaldo.

    Returns:
        Dict con {"correct": bool, "actual": str}.
    """
    prompt = _build_prompt(user_answer)

    try:
        text = bedrock.invoke_with_image(image_base64, media_type, prompt, max_tokens=100)
    except Exception as e:
        if on_fallback:
            on_fallback(e)
        text = nvidia.invoke_with_image(image_base64, media_type, prompt, max_tokens=100)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"correct": False, "actual": "desconocido"}
