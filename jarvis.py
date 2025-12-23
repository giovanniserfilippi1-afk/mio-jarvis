import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configurazione Google Gemini
# La chiave viene letta dalle variabili d'ambiente di Render (GOOGLE_API_KEY)
genai.configure(api_key=os.environ.get("AIzaSyCPieozxxVAmm4oU2Y4JKjgpLUqk9GTvU4"))

app = Flask(__name__)
CORS(app) # Fondamentale per far parlare l'orologio con il server

# Inizializzazione modello
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Ricezione comando
        data = request.json
        domanda = data.get("command", "Nessun comando ricevuto")
        
        # Prompt per la personalità di Jarvis
        prompt = f"Rispondi come Jarvis, l'assistente di Iron Man. Sii conciso, massimo 20 parole: {domanda}"
        
        # Generazione risposta
        response = model.generate_content(prompt)
        
        # PULIZIA: Estraiamo solo il testo ignorando i metadati
        risposta_pulita = response.text.strip()
        
        # Invio risposta al dispositivo
        return jsonify({"reply": risposta_pulita})
    
    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({"reply": "Signore, i sistemi di comunicazione sono offline."}), 500

if __name__ == '__main__':
    # Porta richiesta da Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
