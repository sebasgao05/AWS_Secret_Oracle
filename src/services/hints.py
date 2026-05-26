"""Servicio de generación de pistas crípticas y poéticas."""

from src.clients import bedrock, nvidia


def _build_prompt(hint_number: int, previous_hints: list[str]) -> str:
    """Construye el prompt para generar una pista."""
    previous_hints_text = ""
    if previous_hints:
        previous_hints_text = "\n".join(
            [f"- Pista {i+1}: {h}" for i, h in enumerate(previous_hints)]
        )
        previous_hints_text = (
            f"\n\nPistas anteriores que ya diste (NO repitas ideas):\n{previous_hints_text}"
        )

    return f"""Eres un oráculo misterioso que da pistas sobre imágenes. 
Observa esta imagen y genera UNA SOLA pista críptica y poética (máximo 2 líneas) que ayude a adivinar qué muestra la imagen.

Reglas:
- La pista debe ser metafórica, enigmática y bella.
- NO menciones directamente el objeto/sujeto de la imagen.
- Esta es la pista número {hint_number} de 5. Cada pista debe ser progresivamente más reveladora.
- Pista 1-2: muy abstracta y críptica.
- Pista 3-4: más concreta pero aún poética.
- Pista 5: casi directa pero manteniendo el tono poético.
- Responde SOLO con la pista, sin explicaciones ni prefijos.{previous_hints_text}"""


def generate_hint(
    image_base64: str,
    media_type: str,
    hint_number: int,
    previous_hints: list[str],
    on_fallback=None,
) -> str:
    """Genera una pista críptica usando Claude. Si falla, usa Gemma como respaldo.

    Args:
        image_base64: Imagen en base64.
        media_type: Tipo MIME de la imagen.
        hint_number: Número de pista (1-5).
        previous_hints: Lista de pistas anteriores.
        on_fallback: Callback opcional cuando se usa el modelo de respaldo.

    Returns:
        Texto de la pista generada.
    """
    prompt = _build_prompt(hint_number, previous_hints)

    try:
        return bedrock.invoke_with_image(image_base64, media_type, prompt, max_tokens=150)
    except Exception as e:
        if on_fallback:
            on_fallback(e)
        return nvidia.invoke_with_image(image_base64, media_type, prompt, max_tokens=150)
