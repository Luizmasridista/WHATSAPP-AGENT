
import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Import DeepSeek components
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega as credenciais da Twilio do ambiente
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

# Pega a chave da API do DeepSeek do ambiente
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)

# --- Configuração do Modelo de IA (DeepSeek via LangChain) ---
# Instancia o modelo DeepSeek
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)

# Define um template de prompt para o modelo de IA
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente de IA útil e amigável."),
        ("human", "{question}"),
    ]
)

# Cria uma cadeia LLM com o prompt e o modelo
# Usando a nova sintaxe de encadeamento do LangChain
chain = prompt | llm

# --- Rota para o Webhook do WhatsApp ---
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Pega a mensagem recebida do WhatsApp
    incoming_msg = request.form.get('Body', '')

    # Gera uma resposta usando a cadeia LLM
    # A função invoke é usada para ChatPromptTemplate
    ai_response = chain.invoke({"question": incoming_msg}).content

    # Cria um objeto de resposta TwiML
    resp = MessagingResponse()

    # Adiciona a resposta da IA
    resp.message(ai_response)

    # Retorna a resposta TwiML
    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)