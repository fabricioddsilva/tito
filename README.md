# TiTo: Assistente Virtual para Gerenciamento e Segurança do Laboratório

## Descrição do Projeto
O *TiTo* é um assistente virtual desenvolvido para o gerenciamento e segurança de um laboratório. Ele tem diversas funções como Agendar Visitas, Chatbot, e Controle de Acesso. Onde cada uma dessas funções são dividas em algumas aplicações criadas para englobar o ecosistema do *TiTo* 

## Tecnologias Utilizadas
- *Desenvolvimento*:
  - Python
  - Speech Recognition
  - Selenium
  - pyttsx3
  - OpenAI

## Funcionalidades Principais:

### 1. Marcação de Eventos na Agenda:
- TiTo pode ajudar a criar e agendar novos eventos no nosso site oficial https://kaos-tito.azurewebsites.net/.

### 2. Pequisa Rápida por Voz:
- Você pode fazer perguntas e obter respostas instantâneas utilizando comandos de voz.

## Como Usar:

### 1. Instalação:
- Clone o reposítorio
    ```bash 
    git clone --branch ia https://github.com/fabricioddsilva/tito.git
    ```

- Instale as dependências necessárias utilizando:
    ```bash
    pip install -r requirements.txt 
    ```

### 2. Configuração
- Crie um arquivo `.env` e adicione sua chave de usuário OpenAI nesse modelo:
    `API_KEY = "sua_chave_de_api"`

- No mesmo arquivo adicione o usuário de teste para conseguir criar novos eventos utilizando o comando por voz.
    `USER = "admin"`, `PASSWORD = "w2YtaWAYegfyZBtk6b3NPH3CwkHhUG"`, `REGISTRATION = 7omHFiTAXnMk9GC`

### Execução
- Execute o assistente atráves do comando:
     ```bash
     Python tito.py
     ```
     ou simplesmente inicie atráves da opção em sua IDE

### Comandos Predefinidos
- "*Tito*" é o comando principal para interagir com o assistente.

- "*Tito, como você pode nos ajudar?*" traz uma descrição das funcionalidades do TiTo.

- "*Tito, como você foi feito?*" traz uma descrição pouco técnica de como ele foi criado.








