"""Lógica del estado del juego."""

import streamlit as st

from src.services.hints import generate_hint
from src.services.images import download_image_as_base64, fetch_random_image


def init_game():
    """Inicializa una nueva partida con la primera pista incluida."""
    image_data = fetch_random_image()
    image_url = image_data["url"]
    image_base64, media_type = download_image_as_base64(image_url)

    st.session_state.image_url = image_url
    st.session_state.image_base64 = image_base64
    st.session_state.media_type = media_type
    st.session_state.hints = []
    st.session_state.messages = []
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.actual_name = ""
    st.session_state.hint_count = 0

    # Generar la primera pista automáticamente
    first_hint = generate_hint(image_base64, media_type, 1, [])
    st.session_state.hints.append(first_hint)
    st.session_state.hint_count = 1

    oracle_msg = f"*✨ Pista 1:*\n\n> {first_hint}"
    st.session_state.messages.append(
        {"role": "assistant", "content": oracle_msg, "avatar": "🔮"}
    )
