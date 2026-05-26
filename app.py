"""El Oráculo Visual - Interfaz de usuario con Streamlit."""

import streamlit as st

from src.config import MAX_HINTS
from src.game import init_game
from src.services.hints import generate_hint
from src.services.validation import validate_answer

# --- UI ---
st.set_page_config(page_title="🔮 El Oráculo Visual", page_icon="🔮", layout="centered")

st.title("🔮 El Oráculo Visual")
st.caption("Adivina la imagen a través de pistas crípticas y poéticas. Tienes 5 pistas máximo.")

# Inicializar estado
if "image_url" not in st.session_state:
    with st.spinner("🔮 El oráculo busca una visión..."):
        init_game()

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# Si el juego terminó
if st.session_state.game_over:
    st.divider()
    if st.session_state.won:
        st.success("🎉 ¡Correcto! Has descifrado la visión del oráculo.")
    else:
        st.warning("😔 El oráculo revela su visión...")

    st.image(st.session_state.image_url, caption=f"La respuesta era: {st.session_state.actual_name}")

    if st.button("🔄 Nueva partida", type="primary", use_container_width=True):
        with st.spinner("🔮 El oráculo busca una nueva visión..."):
            init_game()
        st.rerun()
else:
    # Mostrar opciones
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        hint_label = f"💡 Pedir pista ({st.session_state.hint_count}/{MAX_HINTS})"
        hint_disabled = st.session_state.hint_count >= MAX_HINTS
        if st.button(hint_label, disabled=hint_disabled, use_container_width=True):
            with st.spinner("🔮 El oráculo medita..."):

                def _on_fallback(e):
                    st.warning(f"⚠️ Bedrock falló ({type(e).__name__}), usando modelo de respaldo (Gemma)...")

                hint = generate_hint(
                    st.session_state.image_base64,
                    st.session_state.media_type,
                    st.session_state.hint_count + 1,
                    st.session_state.hints,
                    on_fallback=_on_fallback,
                )
                st.session_state.hints.append(hint)
                st.session_state.hint_count += 1
                oracle_msg = f"*✨ Pista {st.session_state.hint_count}:*\n\n> {hint}"
                st.session_state.messages.append(
                    {"role": "assistant", "content": oracle_msg, "avatar": "🔮"}
                )

                if st.session_state.hint_count >= MAX_HINTS:
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "⚠️ Has agotado tus 5 pistas. Escribe tu respuesta o ríndete.",
                            "avatar": "🔮",
                        }
                    )
            st.rerun()

    with col2:
        if st.button("🏳️ Rendirse", type="secondary", use_container_width=True):

            def _on_fallback(e):
                st.warning(f"⚠️ Bedrock falló ({type(e).__name__}), usando modelo de respaldo (Gemma)...")

            validation = validate_answer(
                st.session_state.image_base64,
                st.session_state.media_type,
                "dime qué es la imagen",
                on_fallback=_on_fallback,
            )
            st.session_state.actual_name = validation.get("actual", "Misterio")
            st.session_state.game_over = True
            st.session_state.won = False
            st.session_state.messages.append(
                {"role": "assistant", "content": "🏳️ Te has rendido. El oráculo revela su visión...", "avatar": "🔮"}
            )
            st.rerun()

    # Input del usuario
    if user_input := st.chat_input("Escribe tu respuesta..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("🔮 El oráculo evalúa tu respuesta..."):

            def _on_fallback(e):
                st.warning(f"⚠️ Bedrock falló ({type(e).__name__}), usando modelo de respaldo (Gemma)...")

            validation = validate_answer(
                st.session_state.image_base64,
                st.session_state.media_type,
                user_input,
                on_fallback=_on_fallback,
            )

        if validation.get("correct"):
            st.session_state.actual_name = validation.get("actual", user_input)
            st.session_state.game_over = True
            st.session_state.won = True
            st.session_state.messages.append(
                {"role": "assistant", "content": "🎉 ¡El oráculo asiente! Has descifrado la visión.", "avatar": "🔮"}
            )
        else:
            st.session_state.actual_name = validation.get("actual", "")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "❌ El oráculo niega con la cabeza... Esa no es la respuesta. Sigue intentando o pide otra pista.",
                    "avatar": "🔮",
                }
            )
        st.rerun()
