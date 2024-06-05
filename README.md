# TiTo - Assistente Virtual de Logística
## Sobre o Projeto
TiTo é um assistente virtual de logística desenvolvido para auxiliar em tarefas como agendamento de eventos, pesquisa por voz e controle de entrada e saída de funcionários. Este projeto é uma versão inicial (0.1) e está em constante desenvolvimento.

Funcionalidades Principais
Agendamento de Eventos: TiTo pode criar novos eventos em um site específico, preenchendo campos como nome, data, horário, descrição e quantidade de vagas.
Pesquisa por Voz: O assistente pode responder perguntas e fornecer informações com base em comandos de voz.
Controle de Entrada e Saída: TiTo é capaz de gerenciar a entrada e saída de funcionários através de um sistema integrado.
Requisitos
Python 3.7 ou superior
Bibliotecas Python: openai, speech_recognition, whisper, pyttsx3, selenium, python-dotenv
Instalação
Clone o repositório:

bash
Copiar código
git clone https://github.com/seu_usuario/TiTo.git
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Crie um arquivo .env na raiz do projeto e adicione suas credenciais de API:

plaintext
Copiar código
API_KEY=sua_chave_de_api
USER=seu_usuario
PASSWORD=sua_senha
REGISTRATION=sua_matricula
Execute o script tito.py:

bash
Copiar código
python tito.py
Uso
Você pode interagir com o TiTo através de comandos de voz ou texto.
Para criar um novo evento, diga ou escreva: "Tito, marcar novo evento".
Para fazer uma pergunta, comece com "Tito" ou "tito" seguido da sua pergunta.
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um PR ou uma issue com sugestões, correções ou novas funcionalidades.

Licença
Este projeto está licenciado sob a MIT License.