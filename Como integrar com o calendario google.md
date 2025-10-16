# Como Integrar o Agente com o Google Calendar

Este documento guia você através do processo de configuração da integração do agente de WhatsApp com a API do Google Calendar. Isso é necessário para que o agente possa criar e listar eventos no calendário.

## Pré-requisitos

Antes de começar, você precisará de:

*   Uma conta Google (a conta cujo calendário o agente irá gerenciar).
*   Acesso ao [Google Cloud Console](https://console.cloud.google.com/).
*   Python e `pip` instalados.
*   As dependências do projeto instaladas (`pip install -r memoria do agente/requirements.txt`).

## Passos para Configuração

### 1. Configuração do Projeto no Google Cloud Console

1.  **Crie ou Selecione um Projeto:**
    *   Acesse o [Google Cloud Console](https://console.cloud.google.com/).
    *   No seletor de projetos na parte superior, crie um novo projeto ou selecione um existente.

2.  **Habilite a Google Calendar API:**
    *   No menu de navegação lateral, vá para **"APIs e Serviços" > "Biblioteca"**.
    *   Procure por "Google Calendar API" e clique em **"Ativar"**.

3.  **Crie Credenciais OAuth 2.0:**
    *   No menu de navegação lateral, vá para **"APIs e Serviços" > "Credenciais"**.
    *   Clique em **"+ CRIAR CREDENCIAIS"** e selecione **"ID do cliente OAuth"**.
    *   Se for a primeira vez, você pode ser solicitado a configurar a tela de consentimento OAuth. Siga as instruções, preenchendo as informações necessárias (nome do aplicativo, e-mail de suporte, etc.). Para uso pessoal/teste, você pode configurar como "Externo" e "Tipo de usuário de teste".
    *   Para o **Tipo de aplicativo**, selecione **"Aplicativo de desktop"**.
    *   Dê um nome descritivo (ex: "Agente Google Calendar").
    *   Clique em **"CRIAR"**.

4.  **Baixe o arquivo `credentials.json`:**
    *   Após criar o ID do cliente OAuth, uma caixa de diálogo aparecerá com seu ID do cliente e segredo do cliente.
    *   Clique no botão **"FAZER DOWNLOAD DO JSON"**.
    *   **Renomeie o arquivo baixado para `credentials.json`** (se ele tiver um nome diferente).

### 2. Posicione o arquivo `credentials.json` no Projeto

*   Mova o arquivo `credentials.json` que você acabou de baixar e renomear para o seguinte diretório dentro do seu projeto:
    `whatsapp_agent_ia/Aspectos_do_agente/config/`

### 3. Execute o Script de Autenticação

Este script realizará o fluxo OAuth 2.0, solicitando seu consentimento e gerando o `token.json` necessário para o agente.

1.  **Abra seu terminal ou prompt de comando.**

2.  **Navegue até o diretório do script de autenticação:**
    ```bash
    cd "C:\Users\haneg\OneDrive\Área de Trabalho\Agente de ia\whatsapp_agent_ia\Aspectos_do_agente\config\"
    ```

3.  **Execute o script Python:**
    ```bash
    python authenticate_google_calendar.py
    ```

4.  **Siga as instruções no navegador:**
    *   Uma janela do navegador será aberta, solicitando que você faça login com a conta Google cujo calendário o agente irá gerenciar.
    *   Conceda as permissões solicitadas para o aplicativo acessar seu Google Calendar.
    *   Após a autenticação bem-sucedida, o navegador fechará automaticamente.

5.  **Verifique a criação de `token.json`:**
    *   Um arquivo chamado `token.json` será criado no mesmo diretório do script (`whatsapp_agent_ia/Aspectos_do_agente/config/`). Este arquivo contém as credenciais de acesso e atualização que o agente usará automaticamente em interações futuras.

## Notas Importantes

*   **Segurança:** O arquivo `token.json` contém informações sensíveis. Trate-o como uma senha e **NUNCA o envie para o controle de versão (Git)**. Ele já está incluído no `.gitignore` do projeto.
*   **Reautenticação:** Se o `token.json` for excluído ou se as permissões forem revogadas, você precisará executar o script `authenticate_google_calendar.py` novamente para gerar um novo token.

Com `token.json` no lugar, seu agente estará pronto para interagir com o Google Calendar!
