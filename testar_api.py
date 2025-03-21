import requests

url = "https://assistente-vereador.onrender.com/webhook"

payload = {
    "message": "Olá, como posso solicitar limpeza de rua?",
    "phone": "5513997853222"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status:", response.status_code)
print("Resposta:", response.text)

