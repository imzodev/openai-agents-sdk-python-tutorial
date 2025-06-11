# Tutorial: OpenAI Agents SDK

Este proyecto es un tutorial práctico sobre el uso del [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), un framework ligero y potente para construir aplicaciones agenticas con modelos de lenguaje (LLMs) y herramientas personalizadas en Python.

## ¿Qué es el OpenAI Agents SDK?

El OpenAI Agents SDK permite crear flujos de trabajo multi-agente utilizando un conjunto reducido de primitivas fáciles de aprender:

- **Agentes**: LLMs equipados con instrucciones y herramientas.
- **Handoffs**: Permiten delegar tareas entre agentes.
- **Guardrails**: Validan entradas y salidas para mayor seguridad.
- **Tracing**: Visualiza, depura y monitorea los flujos de agentes.

Es agnóstico de proveedor: soporta tanto APIs de OpenAI como más de 100 otros LLMs.

## Características principales

- Bucle de agente integrado (agent loop).
- Orquestación Python-first: usa funciones y clases estándar de Python.
- Delegación entre agentes (handoffs).
- Validación de entradas/salidas (guardrails).
- Trazabilidad y visualización de flujos.

### Instalación básica

Requisitos: Python 3.8+

1. **Crear un entorno virtual** (recomendado):
   ```bash
   # En Linux/MacOS
   python -m venv vtemp
   source vtemp/bin/activate

   # En Windows
   # python -m venv vtemp
   # vtemp\Scripts\activate
   ```

2. **Instalar dependencias** desde requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todas las dependencias necesarias, incluyendo:
   - `openai-agents`
   - `python-dotenv`
   - Soporte para LiteLLM

### Soporte adicional

Para soporte de voz:

```bash
pip install 'openai-agents[voice]'
```

## Configuración de proveedores de IA

### Configuración del archivo .env

1. Copia el archivo de ejemplo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` con tus credenciales según el proveedor que desees usar:

   #### Google GenAI (configuración predeterminada)
   ```bash
   LLM_API_PROVIDER=google-genai
   LLM_API_KEY=TU_API_KEY_DE_GOOGLE
   LLM_MODEL=gemini-2.5-flash-preview-04-17
   LLM_API_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   ```

   #### Claude (Anthropic)
   ```bash
   LLM_API_PROVIDER=anthropic
   LLM_API_KEY=TU_API_KEY_DE_ANTHROPIC
   LLM_MODEL=claude-3-opus-20240229
   LLM_API_URL=https://api.anthropic.com/v1/
   ```

   #### DeepSeek
   ```bash
   LLM_API_PROVIDER=deepseek
   LLM_API_KEY=TU_API_KEY_DE_DEEPSEEK
   LLM_MODEL=deepseek-chat
   LLM_API_URL=https://api.deepseek.com/v1
   ```

3. Asegúrate de que solo una opción esté descomentada a la vez en el archivo `.env`.

### Instalación de dependencias específicas por proveedor

Dependiendo del proveedor que elijas, podrías necesitar instalar paquetes adicionales:

```bash
export OPENAI_API_KEY=sk-...
```

## Ejemplo básico: Hola Mundo

```python
from agents import Agent, Runner

agent = Agent(name="Asistente", instructions="Eres un asistente útil.")

resultado = Runner.run_sync(agent, "Escribe un haiku sobre la recursión en programación.")
print(resultado.final_output)
```

## Ejemplo de handoffs (delegación entre agentes)

```python
from agents import Agent, Runner
import asyncio

agente_es = Agent(name="Agente Español", instructions="Solo hablas español.")
agente_en = Agent(name="Agente Inglés", instructions="Solo hablas inglés.")

triage_agent = Agent(
    name="Agente Triage",
    instructions="Delegar al agente apropiado según el idioma del mensaje.",
    handoffs=[agente_es, agente_en],
)

async def main():
    resultado = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(resultado.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Ejemplo de herramientas (tools)

```python
from agents import Agent, Runner, function_tool
import asyncio

@function_tool
def obtener_clima(ciudad: str) -> str:
    return f"El clima en {ciudad} es soleado."

agente = Agent(
    name="ClimaBot",
    instructions="Eres un agente útil.",
    tools=[obtener_clima],
)

async def main():
    resultado = await Runner.run(agente, input="¿Qué clima hay en Tokio?")
    print(resultado.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Trazabilidad y depuración

El SDK incluye trazabilidad automática para visualizar y depurar los flujos de agentes. Puedes integrar con herramientas externas como Logfire, AgentOps, Braintrust, Scorecard, y Keywords AI.

Más información sobre tracing: [Documentación de tracing](https://openai.github.io/openai-agents-python/tracing/)

## Recursos útiles

- [Documentación oficial](https://openai.github.io/openai-agents-python/)
- [Repositorio en GitHub](https://github.com/openai/openai-agents-python)
- [Ejemplos de uso](https://github.com/openai/openai-agents-python/tree/main/examples)

## Créditos y agradecimientos

Este SDK se apoya en tecnologías como [Pydantic](https://docs.pydantic.dev/latest/), [MkDocs](https://github.com/squidfunk/mkdocs-material), [Griffe](https://github.com/mkdocstrings/griffe), y [uv](https://github.com/astral-sh/uv).

---

¡Explora, experimenta y construye tus propios agentes inteligentes con este tutorial!
