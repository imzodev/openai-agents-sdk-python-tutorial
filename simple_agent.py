import os
from dotenv import load_dotenv
from agents import Agent, Runner
from openai import AsyncOpenAI
import asyncio
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled

async def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración desde variables de entorno
    base_url = os.getenv("LLM_API_URL", "")
    api_key = os.getenv("LLM_API_KEY", "")
    model_name = os.getenv("LLM_MODEL", "gpt-4")
    
    # Configurar cliente de OpenAI
    client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    
    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)
    
    # Crear un agente simple
    agent = Agent(
        name="Asistente",
        instructions="""Eres un asistente útil y amable que responde preguntas 
        y proporciona información detallada. Sé conciso pero completo en tus respuestas.
        Si no estás seguro de algo, admítelo en lugar de inventar información.""",
        model=model_name,
    )
    
    print("¡Hola! Soy tu asistente. Escribe 'salir' para terminar.")
    print("¿En qué puedo ayudarte hoy?")
    
    while True:
        # Obtener entrada del usuario
        user_input = input("\nTú: ")
        
        # Salir si el usuario lo solicita
        if user_input.lower() in ['salir', 'exit', 'adios', 'chao']:
            print("¡Hasta luego! Ha sido un placer ayudarte.")
            break
            
        # Ejecutar el agente con la entrada del usuario
        try:
            result = await Runner.run(agent, user_input)
            print("\nAsistente:", result.final_output)
        except Exception as e:
            print(f"\nLo siento, ocurrió un error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
