import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Import DeepSeek components
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.agents import AgentFinish

from .tools.ferramentas_do_agente import google_calendar_tools

DATABASE_URL = "sqlite:///../../memoria do agente/chat_history.db"

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

from .Personalidade_do_agente.prompts import prompt

# Define a lógica de janela
K_TURNS = 5  # Manter as últimas 5 interações completas (5 mensagens humanas + 5 mensagens da IA)
K_MESSAGES = K_TURNS * 2

def get_windowed_history(history_messages: list) -> list:
    """
    Pega uma lista completa de mensagens de chat e retorna apenas as últimas K_MESSAGES.
    """
    return history_messages[-K_MESSAGES:]

def format_history(messages: list) -> str:
    formatted_text = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_text += f"Humano: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            formatted_text += f"IA: {msg.content}\n"
    return formatted_text

# Cria uma cadeia LLM com o prompt e o modelo
# Usando a nova sintaxe de encadeamento do LangChain
chain = create_tool_calling_agent(llm, google_calendar_tools, prompt)

agent_executor = AgentExecutor(
    agent=chain,
    tools=google_calendar_tools,
    verbose=True,
    handle_parsing_errors=True
)

# --- Configuração de Memória ---
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy import create_engine

# Define o URI do banco de dados SQLite para o histórico de chat
DATABASE_URL = "sqlite:///chat_history.db"

# Create an engine for SQLAlchemy
engine = create_engine(DATABASE_URL)

# Define o limite de mensagens para a memória persistente (5 turnos = 10 mensagens)
K_PERSISTENT_MESSAGES = 10

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    history = SQLChatMessageHistory(session_id=session_id, connection=engine)
    
    # Poda o histórico se exceder o limite
    if len(history.messages) > K_PERSISTENT_MESSAGES:
        # Mantém apenas as últimas K_PERSISTENT_MESSAGES
        pruned_messages = history.messages[-K_PERSISTENT_MESSAGES:]
        
        # Limpa o histórico existente no banco de dados
        history.clear()
        
        # Adiciona as mensagens podadas de volta ao histórico
        for msg in pruned_messages:
            history.add_message(msg)
            
    return history

# Envolve a cadeia com o histórico de mensagens
with_message_history_chain = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history", # Changed to chat_history
)

# --- Rota para o Webhook do WhatsApp ---
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Pega a mensagem recebida do WhatsApp
    incoming_msg = request.form.get('Body', '')
    from_number = request.form.get('From', '')

    # Usa o número do remetente como ID da sessão
    session_id = from_number

    # Gera uma resposta usando a cadeia LLM com histórico
    ai_response_object = with_message_history_chain.invoke(
        {"input": incoming_msg},
        config={"configurable": {"session_id": session_id}}
    )
    ai_response = ai_response_object["output"]

    # Cria um objeto de resposta TwiML
    resp = MessagingResponse()

    # Adiciona a resposta da IA
    resp.message(ai_response)

    # Retorna a resposta TwiML
    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)