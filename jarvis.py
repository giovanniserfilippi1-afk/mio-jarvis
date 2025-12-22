
import google.generativeai as genai
from flask import Flask, request, jsonify
import json

# Configura Gemini
genai.configure(api_key="AIzaSyCPieozxxVAmm4oU2Y4JKjgpLUqk9GTvU4")

# Istruzioni di sistema per "addestrare" il comportamento
SYSTEM_INSTRUCTION = """
Tu sei JARVIS, l'IA di Tony Stark. 
Sei sofisticato, formale, leggermente sarcastico ma estremamente leale.
Rispondi in italiano. Mantieni le risposte concise per essere lette su uno smartwatch.
Se ti viene chiesto di fare qualcosa, conferma con 'Subito, Signore' o 'Certamente'.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

app = Flask(__name__)
chat_session = model.start_chat(history=[])

@app.route('/jarvis', methods=['POST'])
def process_command():
    data = request.json
    user_query = data.get("command")
    
    # Genera la risposta
    response = chat_session.send_message(user_query)
    
    return jsonify({
        "status": "success",
        "reply": response.text,
        "voice_needed": True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)