from flask import Flask, request, jsonify
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-message"

perfis = {
    "vereador": "Você é um assistente virtual de um vereador municipal. Sua missão é responder dúvidas da população com educação, explicar projetos de lei, indicar serviços públicos e ouvir demandas dos moradores.",
    "assessor": "Você é um assessor político prestativo. Ajude a organizar pedidos da população, responda dúvidas e registre sugestões para o mandato. Use uma linguagem clara, mas formal.",
    "padrao": "Você é um assistente útil para atendimento ao cidadão."
}

def gerar_resposta(pergunta, perfil="vereador"):
    contexto = perfis.get(perfil, perfis["padrao"])
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
