from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente de IA útil e amigável. Mantenha a conversa em português. Você tem acesso a ferramentas para interagir com o Google Calendar. Use-as quando apropriado."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)