from flask import Flask, request, send_file, jsonify
from sesame_ai import TokenManager, SesameWebSocket
import io

app = Flask(__name__)

# Genera un token anonimo all’avvio
token = TokenManager().get_id_token()
# Se vuoi un personaggio diverso, cambia "Miles"
ws = SesameWebSocket(token, character="Miles")

@app.route("/chat", methods=["POST"])
def chat():
    # legge l’audio inviato come body raw (WAV 16kHz mono)
    audio = request.get_data()
    # manda i chunk a Sesame
    ws.send_audio_data(audio)
    # raccoglie la risposta audio
    response_chunks = []
    while True:
        chunk = ws.get_next_audio_chunk()
        if not chunk:
            break
        response_chunks.append(chunk)
    # unisce e restituisce
    out = io.BytesIO(b"".join(response_chunks))
    out.seek(0)
    return send_file(out, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))
