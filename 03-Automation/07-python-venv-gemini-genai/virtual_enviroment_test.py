
from google import genai 
from google.genai import types
import os

chiave=os.environ["GEMINI_API_KEY"]
client=genai.Client(api_key=chiave)


config=types.GenerateContentConfig(
    temperature=0.9,
    max_output_tokens=1024,
    system_instruction="""
    Sei un assistente per la programmazione.
    Rispondi in modo chiaro e semplice.
    Quando puoi usa sempi pratici o annotazioni.
    """
)
while True:
    
    model="gemini-2.5-flash",
    domanda=input(f"-- FAI UNA DOMANDA A GEMINI --\n").strip()
            
    if domanda.lower() in ["exit","esci"]:
        print("Fine sessione...")
        break
    if not domanda: 
        continue
    
    try:
        response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=domanda
        )
        print(f"Gemini: {response.text}")
    except Exception as ex:
        print(f"Errore: {str(ex)}")