import json
from google import genai
from setup.config import settings
from typing import Dict, List, Optional
import io


def generar_examen_ia_json_multiple(texto_base: str, doc: Optional[bytes]) -> Dict[List[Dict], str]:
    """
    Genera preguntas de examen de opción múltiple (4 opciones)
    intentando obtener una respuesta JSON válida de Gemini.
    (Esta función es la misma que la versión anterior)
    """
    if not texto_base:
        raise Exception("ERROR: El texto base para generar el examen está vacío.")
 
    prompt_estructurado_json = f"""
    **Contexto:** Eres un asistente de IA experto en crear evaluaciones educativas en formato JSON estructurado. Tu tarea es generar preguntas de examen **exclusivamente de opción múltiple con 4 opciones (a, b, c, d)**, basadas **estrictamente** en el texto proporcionado y siguiendo las instrucciones específicas. Debes devolver **únicamente** un objeto JSON válido, sin ningún texto adicional antes o después (ni siquiera ```json ... ```).

    **Instrucciones del Profesor (enfocadas en Opción Múltiple):**
    "{texto_base}"

    **Formato JSON Requerido para la Salida (Estrictamente Opción Múltiple):**
    La salida debe ser un objeto JSON que contenga una única clave llamada "examen". El valor de "examen" debe ser una lista (array) de objetos JSON, donde cada objeto representa una pregunta de opción múltiple.
    Cada objeto de pregunta DEBE tener los siguientes campos:
    - "numero": (Integer) El número consecutivo de la pregunta (empezando en 1).
    - "tipo": (String) DEBE ser siempre el valor exacto "opcion_multiple".
    - "pregunta_texto": (String) El texto completo de la pregunta.
    - "opciones": (List/Array) Una lista que contenga **exactamente 4 objetos**, cada uno representando una opción. Cada objeto de opción debe tener:
        - "opcion_letra": (String) La letra de la opción ('a', 'b', 'c', 'd').
        - "opcion_texto": (String) El texto de la opción.
    - "respuesta_correcta_letra": (String) La letra ('a', 'b', 'c', o 'd') correspondiente a la opción correcta.

    **Reglas Muy Importantes:**
    1.  **Todas** las preguntas generadas deben ser de **opción múltiple** con **exactamente 4 opciones**.
    2.  Genera las preguntas basándote **únicamente** en la información del "Texto Base". No inventes datos.
    3.  Sigue las "Instrucciones del Profesor" en cuanto a cantidad y dificultad de las preguntas (siempre serán de opción múltiple).
    4.  La respuesta COMPLETA debe ser **solamente el objeto JSON**, empezando con `{{"examen": [...]}}` y terminando con `}}`. Sin comentarios, sin explicaciones, sin marcadores de código.

    **Ejemplo de Estructura de Salida JSON Válida (SOLO Opción Múltiple, 4 opciones):**
        ```json
        {{
        "examen": [
            {{
            "numero": 1,
            "tipo": "opcion_multiple",
            "pregunta_texto": "¿Cuál es el principal producto gaseoso liberado durante la fotosíntesis?",
            "opciones": [
                {{"opcion_letra": "a", "opcion_texto": "Dióxido de carbono"}},
                {{"opcion_letra": "b", "opcion_texto": "Nitrógeno"}},
                {{"opcion_letra": "c", "opcion_texto": "Oxígeno"}},
                {{"opcion_letra": "d", "opcion_texto": "Hidrógeno"}}
            ],
            "respuesta_correcta_letra": "c"
            }},
            {{
            "numero": 2,
            "tipo": "opcion_multiple",
            "pregunta_texto": "¿En qué organelo celular ocurre principalmente la fotosíntesis?",
            "opciones": [
                {{"opcion_letra": "a", "opcion_texto": "Mitocondria"}},
                {{"opcion_letra": "b", "opcion_texto": "Núcleo"}},
                {{"opcion_letra": "c", "opcion_texto": "Ribosoma"}},
                {{"opcion_letra": "d", "opcion_texto": "Cloroplasto"}}
            ],
            "respuesta_correcta_letra": "d"
            }}
        ]
        }}
        ```
    """ 

    try:

        model = genai.Client(api_key=settings.gemini_api_key)
        
        contents = [prompt_estructurado_json]

        if doc: 
            sample_doc = model.files.upload(
                # You can pass a path or a file-like object here
                file=io.BytesIO(doc),
                config=dict(
                    mime_type='application/pdf')
                )
            contents=[sample_doc, prompt_estructurado_json]
        
        response = model.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )

        if response.text:
            try:
                clean_text = response.text.strip()
                if clean_text.startswith("```json"): clean_text = clean_text[7:]
                if clean_text.endswith("```"): clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
                parsed_json = json.loads(clean_text)

                if "examen" in parsed_json and isinstance(parsed_json["examen"], list):
                    return parsed_json["examen"]
                else:
                    error_msg = "ERROR: El JSON recibido no tiene la estructura esperada (falta la clave 'examen' o no es una lista)."
                    return error_msg
            except json.JSONDecodeError as json_err:
                error_msg = f"ERROR: La respuesta del modelo no es un JSON válido. {json_err}"
                return error_msg
            except Exception as parse_err:
                 error_msg = f"ERROR: Ocurrió un error al procesar la respuesta JSON. {parse_err}"
                 return error_msg
        else:
             try:
                 block_reason = response.prompt_feedback.block_reason; block_message = response.prompt_feedback.block_reason_message
                 error_msg = f"ERROR: La generación de contenido fue bloqueada. Razón: {block_reason} - {block_message}"
             except AttributeError:
                 if response.candidates and response.candidates[0].finish_reason != 'STOP': error_msg = f"ERROR: La generación no se completó correctamente. Razón: {response.candidates[0].finish_reason}"
                 else: error_msg = "ERROR: La respuesta de la API no contiene texto generado por una razón desconocida."
             print(error_msg)
             return error_msg
    except Exception as e:
        error_msg = f"ERROR: Ocurrió un error durante la llamada a la API de Gemini: {e}"
        print(error_msg)
        return error_msg