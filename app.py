import streamlit as st
from google import genai
from google.genai import types
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Creemos tu imagen", page_icon="🍌")
st.title("vos decinos qué pensas y nosotros creamos")


# --- 2. CREDENCIALES (BARRA LATERAL) ---
with st.sidebar:
    api_key = st.text_input("Ingresa tu Google API Key:", type="password")
    if api_key:
        # Inicializamos el cliente nativo de Google (sin LangChain)
        client = genai.Client(api_key=api_key)

# --- 3. INTERFAZ CREATIVA ---
description = st.text_area("¿Qué quieres generar?", placeholder="Una ciudad futurista con coches voladores...")

style = st.radio(
    "Elige un estilo:",
    ['Photorealistic', 'Cartoon', 'Oil Painting', 'Cyberpunk'],
    horizontal=True
)

# --- 4. ACCIÓN Y LLAMADA A NANO BANANA ---
if st.button("🎨 Generar Imagen"):
    if not api_key:
        st.error("Por favor, pon tu API Key en la barra lateral.")
    elif not description:
        st.warning("Escribe una descripción primero.")
    else:
        # Unimos el prompt
        full_prompt = f"Create an image of {description} in a {style} style."
        
        with st.spinner("Pintando la imagen..."):
            try:
                # LA LLAMADA CRÍTICA (Basado en el Plano B)
                response = client.models.generate_content(
                    model='gemini-2.5-flash-image',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['IMAGE'] # Obligamos a que devuelva imagen
                    )
                )
                
                # PROCESANDO LOS BYTES
                for part in response.parts:
                    if part.inline_data:
                        image_bytes = part.inline_data.data
                        # Renderizamos la imagen en la web
                        st.image(
                            image_bytes, 
                            caption=f'Estilo: {style}', 
                            use_container_width=True
                        )
                        st.balloons()
            except Exception as e:
                st.error(f"Ocurrió un error en la generación: {e}")
