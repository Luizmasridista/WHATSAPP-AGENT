# Roadmap: Agendador de Reuniões (Google Calendar)

Este documento descreve o roadmap para implementar a funcionalidade de agendamento de reuniões no Google Calendar para o agente de IA.

---

## Visão Geral

O objetivo é permitir que o agente de IA, através de comandos do usuário no WhatsApp, possa criar, listar e gerenciar eventos no Google Calendar. Isso será feito integrando a API do Google Calendar como uma ferramenta no framework LangChain.

---

## Fases de Implementação

### Fase 1: Configuração e Autenticação da API do Google Calendar

1.  **Configuração do Projeto Google Cloud:**
    *   Criar um novo projeto no Google Cloud Console (se ainda não houver um).
    *   Habilitar a "Google Calendar API" para o projeto.
    *   Criar credenciais OAuth 2.0 (tipo "Aplicativo de desktop" ou "Aplicativo da Web", dependendo da estratégia de autorização do agente).
    *   Baixar o arquivo `credentials.json` e salvá-lo em um local seguro (ex: `whatsapp_agent_ia/Aspectos do agente/`). **(FEITO - `credentials.json` baixado e colocado em `whatsapp_agent_ia/Aspectos do agente/`)**

2.  **Instalação de Dependências:**
    *   Adicionar `google-api-python-client` e `google-auth-oauthlib` ao `requirements.txt` (localizado em `memoria do agente/`). **(FEITO)**
    *   Instalar as novas dependências: `pip install -r memoria do agente/requirements.txt`. **(FEITO)**

3.  **Implementação do Fluxo de Autenticação OAuth 2.0:**
    *   Desenvolver um script Python separado para realizar o fluxo de autenticação inicial. Este script obterá o consentimento do usuário e gerará um `token.json` (contendo o token de acesso e o refresh token). **(FEITO)**
    *   O `token.json` deve ser salvo em um local seguro (ex: `whatsapp_agent_ia/Aspectos do agente/`). **(FEITO - `token.json` gerado e salvo após execução manual do script de autenticação)**
    *   A lógica do agente usará este `token.json` para autenticar-se automaticamente em interações futuras.

### Fase 2: Definição da Ferramenta LangChain para Google Calendar

1.  **Criação da Ferramenta no `ferramentas_do_agente.py`:**
    *   Criar uma função Python que utilize a biblioteca `google-api-python-client` para interagir com a API do Google Calendar. **(FEITO)**
    *   Exemplo de funções a serem implementadas:
        *   `create_calendar_event(summary: str, start_datetime: str, end_datetime: str, attendees: list = None, description: str = None)`: Para criar um novo evento. **(FEITO)**
        *   `list_upcoming_events(max_results: int = 10)`: Para listar eventos futuros. **(FEITO)**
    *   Envolver essas funções como ferramentas LangChain usando `Tool` ou `StructuredTool`. **(FEITO)**

2.  **Integração da Ferramenta com o Agente:**
    *   No `cerebro_do_agente.py`, importar a(s) nova(s) ferramenta(s) do `ferramentas_do_agente.py`. **(FEITO)**
    *   Adicionar a(s) ferramenta(s) à lista de ferramentas que o agente pode utilizar. **(FEITO - A integração está funcional, e o agente está tentando usar as ferramentas. Erros iniciais de formatação de prompt e passagem de argumentos foram tratados.)**

### Fase 3: Teste e Refinamento

1.  **Testes Unitários para a Ferramenta:**
    *   Criar testes unitários para garantir que a ferramenta do Google Calendar interaja corretamente com a API (pode-se usar mocks para a API durante os testes).
2.  **Testes de Integração do Agente:**
    *   Testar o agente completo via WhatsApp, solicitando o agendamento de reuniões e a listagem de eventos.
    *   Refinar o `PromptTemplate` e as instruções do agente para otimizar a capacidade do LLM de decidir quando e como usar a ferramenta do Google Calendar.
3.  **Tratamento de Erros:**
    *   Implementar tratamento de erros robusto para falhas na API, problemas de autenticação e entradas inválidas do usuário.

---

## Considerações Adicionais

*   **Melhorias Estruturais:** Para melhor organização e compatibilidade com pacotes Python, os diretórios `Aspectos do agente` e `Personalidade do agente` foram renomeados para `Aspectos_do_agente` e `Personalidade_do_agente`, respectivamente. Arquivos `__init__.py` foram adicionados aos diretórios `Aspectos_do_agente`, `Aspectos_do_agente/config`, `Aspectos_do_agente/tools` e `Aspectos_do_agente/Personalidade_do_agente` para garantir o correto funcionamento das importações relativas. O script `authenticate_google_calendar.py` e o arquivo `credentials.json` foram movidos para `Aspectos_do_agente/config/`.
*   **Segurança:** Garantir que o `credentials.json` e `token.json` sejam armazenados de forma segura e que o acesso à API seja o mínimo necessário.
*   **Experiência do Usuário:** Pensar em como o agente irá confirmar agendamentos, lidar com conflitos de horário e fornecer feedback ao usuário.
*   **Escalabilidade:** Se o agente for para produção, considerar como a autenticação e o armazenamento de tokens serão gerenciados para múltiplos usuários.
