from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, handoff, InputGuardrailTripwireTriggered, input_guardrail
import asyncio
from pydantic import BaseModel


class ClasificacionPregunta(BaseModel):
    is_matematicas: bool
    razonamiento: str

# Agente clasificador
agente_clasificador =  Agent(
    name="Clasificador de Preguntas",
    instructions="""Clasifica la pregunta como matemática o no matemática.
    Devuelve un JSON con:
    - is_matematicas: true si es sobre matemáticas, false en caso contrario
    - razonamiento: una explicación breve de tu decisión
    """,
    model="gpt-4o-mini",
    output_type=ClasificacionPregunta
)

async def clasificar_pregunta(ctx: RunContextWrapper[None], agent: Agent, input: str):
    clasificacion = await Runner.run(agente_clasificador, input, context=ctx.context)
    return clasificacion.final_output_as(ClasificacionPregunta)

@input_guardrail
async def solo_matematicas(ctx, agent, input):
    clasificacion = await clasificar_pregunta(ctx, agent, input)
    if not clasificacion.is_matematicas:
        return GuardrailFunctionOutput(
            output_info=clasificacion,
            tripwire_triggered=True,
        )
    else:
        return GuardrailFunctionOutput(
            output_info=clasificacion,
            tripwire_triggered=False,
        )

# Agente experto en matemáticas
agente_matematicas = Agent(
    name="Experto en Matemáticas",
    instructions="Eres un tutor de matemáticas. Ayuda a resolver problemas con explicaciones claras y paso a paso.",
    model="gpt-4o-mini",
    handoff_description="Para preguntas sobre matemáticas"
)


# Agente enrutador principal
agente_router = Agent(
    name="Enrutador de Preguntas",
    instructions="""Dirige las preguntas al experto adecuado según el tema.
    No respondas preguntas directamente.""",
    model="gpt-4o-mini",
    handoffs=[agente_matematicas],
    input_guardrails=[solo_matematicas]
)

async def main():
    preguntas = [
        "¿Cuánto es 2+2?",
        "¿Quién es LeBron James?",
        "¿Cómo resuelvo la ecuación x^2 - 4 = 0?",
        "¿Cuándo fue la Segunda Guerra Mundial?",
        "¿Cuál es la derivada de x^3?",
        "¿Qué es la fotosíntesis?"
    ]
    
    for pregunta in preguntas:
        print(f"\n=== Pregunta: {pregunta} ===")
        try:
            respuesta = await Runner.run(agente_router, pregunta)
            print(f"Respuesta: {respuesta.final_output[:50]}...")
        except InputGuardrailTripwireTriggered:
            print("Lo siento, solo puedo responder preguntas de matemáticas.")

if __name__ == "__main__":
    asyncio.run(main())