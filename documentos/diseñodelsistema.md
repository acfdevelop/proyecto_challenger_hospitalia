                    USUARIO
                       │
                       ▼
            "¿Qué necesito para hospitalizarme?"
                       │
                       ▼
                   app.py
         (Recibe la pregunta del usuario)
                       │
                       ▼
                  agente.py
          (Orquesta todo el flujo)
                       │
                       ▼
                 Nodo Triaje
                 (triaje.py)
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
AUTO_RESOLVER     PEDIR_INFO    ABRIR_TICKET
         │
         ▼
       rag.py
(Busca información en los PDFs)
         │
         ▼
   Vector Store (Chroma)
         │
         ▼
 Recupera los mejores chunks
         │
         ▼
       Gemini
(Genera la respuesta usando
solo el contexto encontrado)
         │
         ▼
      Respuesta final
         │
         ▼
        Usuario


¿Qué hace cada archivo?
app.py

Solo conversa con el usuario.

Ejemplo:

Usuario escribe

↓

envía la pregunta

↓

muestra la respuesta

No hace inteligencia.

agente.py

Es el "jefe".

No responde preguntas.

Solo decide:

Primero triaje

↓

Después RAG

↓

Después respuesta
triaje.py

Lee la pregunta.

Ejemplo:

¿Cómo retiro mis exámenes?

↓

Decide

AUTO_RESOLVER

Otro ejemplo

Quiero presentar un reclamo.

↓

Puede decidir

ABRIR_TICKET
rag.py

Es el cerebro documental.

Hace esto:

Pregunta

↓

Embeddings

↓

Busca en Chroma

↓

Recupera documentos

↓

Gemini responde
documentos/

Es el conocimiento.

No hay IA aquí.

Solo información.

Vector Store

Aquí ocurre la magia.

Tus PDFs se transforman en vectores.

Después ya no se leen nuevamente.

Por eso existe esta carpeta.

Lo que más quiero que entiendas

Cuando preguntes

¿Qué necesito para hospitalizarme?

Gemini NO responde inmediatamente.

Hace esto.

Pregunta

↓

Busca en el Vector Store

↓

Encuentra

02_Hospitalizacion.pdf

↓

Extrae cuatro fragmentos

↓

Los envía a Gemini

↓

Gemini responde usando SOLO esos fragmentos

Eso es un RAG.

Después entra LangGraph

Y aquí viene lo que más querías aprender.

En realidad LangGraph no sabe nada del hospital.

Solo mueve un diccionario.

Imagina esto:

state = {
    "pregunta": "¿Qué necesito para hospitalizarme?"
}

El primer nodo recibe:

{
    "pregunta": "¿Qué necesito para hospitalizarme?"
}

Después devuelve:

{
    "triaje": {
        "decision": "AUTO_RESOLVER"
    }
}

LangGraph mezcla automáticamente ambos diccionarios y el estado pasa a ser:

state = {
    "pregunta": "¿Qué necesito para hospitalizarme?",
    "triaje": {
        "decision": "AUTO_RESOLVER"
    }
}

Luego el siguiente nodo (rag) recibe todo ese estado.

Después devuelve:

{
    "respuesta": "...",
    "contexto": [...],
    "encontrado": True
}

Ahora LangGraph vuelve a unir todo:

state = {

    "pregunta": "...",

    "triaje": {...},

    "respuesta": "...",

    "contexto": [...],

    "encontrado": True
}

¿Te das cuenta?

Ningún nodo necesita llamar al otro directamente.

Cada nodo solo:

recibe un diccionario (state)
hace su trabajo
devuelve otro diccionario

Y LangGraph se encarga del resto.

Creo que cuando entiendas esta idea, dejarás de ver LangGraph como algo "mágico".

tengo esta estructura .venv documentos/ vectorstore/ .env .gitignore agente.py app.py prompts.py rag.py README.md triaje.py esta estructura me la diste de un inicio