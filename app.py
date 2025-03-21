from flask import Flask, request, jsonify
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configurações da Z-API
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-message"

# Inicializa a aplicação Flask
app = Flask(__name__)

# Rota inicial para teste
@app.route("/")
def home():
    return "Assistente do vereador está rodando corretamente!"

# Função que gera a resposta usando o ChatGPT (OpenAI 1.x)
def gerar_resposta(mensagem):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Responda de forma educada e objetiva a mensagem: {mensagem}"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente virtual de um vereador municipal. Responda com respeito, clareza e foco em ajudar o cidadão."},
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content.strip()

# Rota webhook para receber mensagens do WhatsApp via Z-API
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    mensagem = data.get("message")
    telefone = data.get("phone")

    if not mensagem or not telefone:
        return jsonify({"erro": "Mensagem ou telefone ausente"}), 400

    resposta = gerar_resposta(mensagem)

    payload = {
        "phone": telefone,
        "message": resposta
    }

    r = requests.post(ZAPI_URL, json=payload)
    return jsonify({"status": "enviado", "resposta": resposta})

# Rodar localmente ou no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
