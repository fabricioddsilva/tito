#Importando as Bibliotecas
import openai
import speech_recognition as sr
import whisper
import pyttsx3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
from dotenv import load_dotenv
import requests
from datetime import datetime


load_dotenv()

#Chave da API
openai.api_key = os.getenv("API_KEY")

# caso nao queira falar "assistente" ou "Chat GPT"
sem_palavra_ativadora = False
# printa o total de tokens por interacao
debug_custo = False
# print de algumas informacoes para debug
debugar = False
# define qual gerador de texto
# escolher_stt = "whisper"
escolher_stt = "google"
# escolhe entrada por texto ou voz
entrada_por_texto = False
# falar ou nao
falar = True

if entrada_por_texto:
    sem_palavra_ativadora = True

#Configura o Gerador de Mensagens
def generate_answer(messages):
    #response = openai.ChatCompletion.create( ## Api antiga
    response = openai.chat.completions.create( ## API nova
        model="gpt-3.5-turbo",  ##
        messages=messages,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

#Configura a resposta por áudio
def talk(texto):
    # falando
    engine.say(texto)
    engine.runAndWait()
    engine.stop()

#Configura o salvamento de dados
def save_file(dados):
    with open(path + filename, "wb") as f:
        f.write(dados)
        f.flush()
        
#Configura valores a serem recebidos do usuário por meio de voz
def input_por_voz():
    resposta = ""
    while True:
        with mic as fonte:
            audio = r.listen(fonte)
        try:
            resposta = r.recognize_google(audio, language="pt-BR")
            print("Você disse:", resposta)
            break
        except sr.UnknownValueError:
            print("Desculpe, não entendi. Poderia repetir?")
            talk("Desculpe, não entendi. Poderia repetir?")
        except sr.RequestError:
            print("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
            talk("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
    return resposta

#Dicionario usado para converter os meses por extenso para número
meses = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12"
}

#Função para converter meses por extenso para número
def formatar_data(data):
    try:
        # Remover "de" e "do" da data
        data_formatada = re.sub(r'\b(de|do)\b', '', data)
        # Converter o nome do mês para seu valor numérico
        for mes, valor in meses.items():
            if mes in data_formatada:
                data_formatada = data_formatada.replace(mes, valor)
        # Remover espaços em branco
        data_formatada = data_formatada.replace(' ', '')
    except sr.UnknownValueError:
            print("Desculpe, não entendi. Poderia repetir?")
            talk("Desculpe, não entendi. Poderia repetir?")
    except sr.RequestError:
            print("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
            talk("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
    return data_formatada

#Função para formatação do horário
def converter_horario(horario):
    hora = 0
    minutos = 0
    try:
        # Verificar se "da manhã", "da tarde" ou "da noite" está presente na entrada
        if "uma da manhã" in horario or "1 hora da manhã" in horario or "1:00 da manhã" in horario:
            horario = "1:00"
        elif "duas da manhã" in horario or "2 horas da manhã" in horario or "2:00 da manhã" in horario :
            horario = "2:00"
        elif "meio dia" in horario or "meio-dia" in horario:
            horario = "12:00"
        elif "uma da tarde" in horario or "1 hora da tarde" in horario or "1:00 da tarde" in horario:
            horario = "13:00"
        elif "duas da tarde" in horario or "2 horas da tarde" in horario or "2:00 da tarde" in horario:
            horario = "14:00"
        elif "da manhã" in horario or "horas da manhã" in horario:
            
            if "horas da manhã" in horario:
                horario = horario.replace("horas da manhã", "")
            elif "da manhã" in horario:
                horario = horario.replace("da manhã", "")
                
            partes = re.split(r":", horario)
            hora = int(partes[0])
            minutos = int(partes[1])
            # Se a hora for 12, torná-la 0 para representar 12:00 AM
            hora = hora if hora != 12 else 0
        elif "da tarde" in horario or "horas da tarde" in horario:
            
            if "horas da tarde" in horario:
                horario = horario.replace("horas da tarde", "")
            elif "da tarde" in horario:
                horario = horario.replace("da tarde", "")
            
            
            partes = re.split(r":", horario)
            hora = int(partes[0])   # Adicionar 12 horas para representar PM
            minutos = int(partes[1])
            # Se a hora for 12 PM, manter 12, caso contrário, adicionar 12 horas
            hora = hora if hora == 12 else hora + 12
        elif "da noite" in horario or "horas da noite" in horario:
            
            if "horas da noite" in horario:
                horario = horario.replace("horas da noite", "")
            elif " da noite" in horario:
                horario = horario.replace("da noite", "")
            
            partes = re.split(r":", horario)
            hora = int(partes[0])
            minutos = int(partes[1])
            # Se a hora for 12, torná-la 0 para representar 12:00 AM
            hora = hora if hora != 12 else 0
            # Adicionar 12 horas para representar AM
            hora += 12
        else:
            print("Não entendi. Por favor, tente novamente.")
            return None

    except sr.UnknownValueError:
        print("Desculpe, não entendi. Poderia repetir?")
        talk("Desculpe, não entendi. Poderia repetir?")
    except sr.RequestError:
            print("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
            talk("Desculpe, ocorreu um erro durante o reconhecimento de voz.")

    return f"{hora:02d}:{minutos:02d}"





# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

# falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Selecionar a primeira voz disponível
if voices:
    voz_padrao = voices[0]
    engine.setProperty('voice', voz_padrao.id)
    print("Usando a voz padrão:", voz_padrao.name)
else:
    print("Nenhuma voz encontrada. Usando a configuração padrão.")

engine.setProperty('rate', 180)  # velocidade 120 = lento

mensagens = [{"role": "system", "content": "Você é um assistente gente boa. E meu nome é Fabrício!"}]

path = os.getcwd()
filename = "audio.wav"

print("Speak to Text", escolher_stt)

ajustar_ambiente_noise = True

#Loop principal com todas as funções
while True:
    try:
        text = ""
        question = ""

        if entrada_por_texto:
            question = input("Perguntar pro Tito (\"sair\"): ")
        else:
            # Faça uma pergunta
            with mic as fonte:
                if ajustar_ambiente_noise:
                    r.adjust_for_ambient_noise(fonte)
                    ajustar_ambiente_noise = False
                print("Fale alguma coisa")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")
            
            #Escolha do modelo de reconhecimento
                if escolher_stt == "google":
                    question = r.recognize_google(audio, language="pt-BR")
                elif escolher_stt == "whisper":
                    save_file(audio.get_wav_data())

            if escolher_stt == "whisper":
                text = model.transcribe(path + filename, language='pt', fp16=False)
                question = text["text"]

        #Condição para encerrar o aplicativo 
        if ("esligar" in question and "Tito" in question) or question.startswith("sair"):
            print(question, "Saindo.")
            if falar:
                talk("Desligando")
            break
        elif question == "":
            print("No sound")
            continue
        #Palavra chave para se comunicar com o TiTo
        elif question.startswith("Tito") or question.startswith("tito"):
            
            #Primeira pergunta pre-programada:
            if "como você pode nos ajudar" in question or "Como você pode nos ajudar" in question:
                resposta_tito = "Olá, eu sou a versão 0.1 do TiTo, um assistente virtual que busca resolver alguns problemas de logística, com as 3 funções iniciais: marcar eventos na agenda da empresa, fazer pesquisas rápidas por voz e administrar a saída e entrada de funcionários pelo 'TiTo AiOuTi'. Vai ser um prazer ajudar na inovação do método que vemos os laboratórios"
                print("Me: ", question)
                print("Tito:", resposta_tito)
                mensagens.append({"role": "user", "content": str(question)})
                mensagens.append({"role": "assistant", "content": resposta_tito})
                if falar:
                    talk(resposta_tito)
                    
            #Segunda pergunta pre-programada:
            elif "como você foi feito" in question or "Como você foi feito" in question:
                resposta = "Eu sou um modelo que foi desenvolvido pela OupenEiAi, e que foi modificado usando a linguagem de programação Python para atender a solução. Usando várias bibliotecas da linguagem de programação, por exemplo a biblioteca de reconhecimento de fala que me permite escutar e assim tirar as suas dúvidas, e também outras bibliotecas que me permitem fazer funções únicas como criar um novo evento no nosso site oficial."
                print("Me:", question)
                print("Tito:", resposta)
                if falar:
                    talk(resposta)
                    
            elif "qual evento" in question and "recente" in question or "qual evento" in question and "próximo":
                response = requests.get('http://127.0.0.1:5000/evento')
                data = response.json()[0]['data_evento']
                data_convert = datetime.strptime(data, "%Y-%m-%d")
                data_atual = datetime.now()
                tempo_restante = data_convert.day - data_atual.day
                hora_inicio = response.json()[0]['hora_inicio']
                hora_fim = response.json()[0]['hora_fim']
                visitantes = response.json()[0]['visitantes']
                nome = response.json()[0]['nome']
                
                if tempo_restante == 1:
                    resposta = f"O evento mais recente é o {nome} que acontecerá amanhã das {hora_inicio} até {hora_fim}"
                else:
                    resposta = f"O evento mais recente é o {nome} que acontecerá daqui a {tempo_restante} dias, das {hora_inicio} até {hora_fim}"
                print("Me: ", question)
                print("Tito: ", resposta)
                if falar:
                    talk(resposta)
            
            #Condicional para criação de um novo evento usando a aplicação de criação de eventos
            elif "Marcar novo evento" in question or "marcar Novo Evento" in question or "Marcar Novo Evento" in question or "Novo Evento" in question or "novo evento" in question or "Criar Novo Evento" in question or "criar novo evento" in question:
                print("Abrindo o navegador Chrome e indo para o site do evento...")
                # Abrir o navegador Chrome
                driver = webdriver.Chrome()
                # Navegar até o site
                driver.get("http://127.0.0.1:5000//login")
                # Esperar alguns segundos para a página carregar completamente
                time.sleep(1)
                # Preencher os campos do formulário
                driver.find_element(By.NAME, "usuario").send_keys(os.getenv("USER"))
                driver.find_element(By.NAME, "senha").send_keys(os.getenv("PASSWORD"))
                driver.find_element(By.NAME, "matricula").send_keys(os.getenv("REGISTRATION"))
                # Submeter o formulário
                driver.find_element(By.ID,"submit").click()
                driver.get("http://127.0.0.1:5000//evento/novo")
                
                if falar:
                    print("Preenchendo o campo nome...")
                    talk("Qual o nome do evento?")
                    nome = input_por_voz()
                    driver.find_element(By.NAME, "nome").send_keys(nome)
                    print("Navegação concluída.")
                    
                if falar:
                        print("Preenchendo o campo data...")
                        talk("Qual a data desse evento?")
                        data = input_por_voz()
                        data_formatada = formatar_data(data)
                        driver.find_element(By.NAME, "data").send_keys(data_formatada)
                        
                if falar:
                        print("Preenchendo o campo hora inicial...")
                        talk("Qual o horário de inicio do evento?")
                        hora_inicio = input_por_voz()
                        if converter_horario(hora_inicio) == None:
                                    hora_inicio = input_por_voz()
                                    hora_inicio_formatada = converter_horario(hora_inicio)
                                    driver.find_element(By.NAME, "hora_inicio").send_keys(hora_inicio_formatada)
                        else:
                                hora_inicio_formatada = converter_horario(hora_inicio)
                                driver.find_element(By.NAME, "hora_inicio").send_keys(hora_inicio_formatada)
                                
                if falar:
                        print("Preenchendo o campo hora de termino...")
                        talk("Qual o horário de termino do evento?")
                        hora_fim = input_por_voz()
                        if converter_horario(hora_fim) == None:
                                        hora_fim = input_por_voz()
                                        hora_fim_formatada = converter_horario(hora_fim)
                                        driver.find_element(By.NAME, "hora_fim").send_keys(hora_fim_formatada)
                        else:
                                        hora_fim_formatada = converter_horario(hora_fim)
                                        driver.find_element(By.NAME, "hora_fim").send_keys(hora_fim_formatada)
                                        
                if falar:
                        print("Preenchendo o campo hora de descrição...")
                        talk("Qual a descrição do evento?")
                        descricao = input_por_voz()
                        driver.find_element(By.NAME, "descricao").send_keys(descricao)
                        
                if falar:
                    print("Preenchendo o campo quantidade de visitantes...")
                    talk("Qual seria a quantidade de vagas para esse evento?")
                    vagas = input_por_voz()
                    driver.find_element(By.NAME, "visitantes").send_keys(vagas)
                    confirmacao = False
                    while not confirmacao:
                        print("Confirmando os dados inseridos...")
                        talk("Verifique os dados inseridos. Deseja confirmar?")
                        resposta = input_por_voz().lower()
                        
                        if "sim" in resposta or "Sim" in resposta:
                            confirmacao = True
                            # Submeter o formulário
                            driver.find_element(By.ID,"submit").click()
                            print("Formulário submetido com sucesso!")
                            
                        elif "não" in resposta or "nao" in resposta:
                            # Perguntar qual campo deseja alterar
                            print("Qual campo você deseja alterar?")
                            talk("Qual campo você deseja alterar?")
                            campo_alterar = input_por_voz().lower()
                            
                            if "nome" in campo_alterar:
                                talk("Qual o novo nome do evento?")
                                nome = input_por_voz()
                                driver.find_element(By.NAME, "nome").clear()
                                driver.find_element(By.NAME, "nome").send_keys(nome)
                            
                            elif "data" in campo_alterar:
                                talk("Qual a nova data do evento?")
                                data = input_por_voz()
                                data_formatada = formatar_data(data)
                                driver.find_element(By.NAME, "data").clear()
                                driver.find_element(By.NAME, "data").send_keys(data_formatada)
                                
                            elif "hora de inicio" in campo_alterar:
                                talk("Qual o novo horário de inicio do evento?")
                                hora_inicio = input_por_voz()
                                if converter_horario(hora_inicio) == None:
                                    hora_inicio = input_por_voz()
                                    hora_inicio_formatada = converter_horario(hora_inicio)
                                    driver.find_element(By.NAME, "hora_inicio").clear()
                                    driver.find_element(By.NAME, "hora_inicio").send_keys(hora_inicio_formatada)
                                else:
                                    hora_inicio_formatada = converter_horario(hora_inicio)
                                    driver.find_element(By.NAME, "hora_inicio").clear()
                                    driver.find_element(By.NAME, "hora_inicio").send_keys(hora_inicio_formatada)
                                    
                            elif "hora de término" in campo_alterar:
                                talk("Qual o novo horário de término do evento?")
                                hora_fim = input_por_voz()
                                if converter_horario(hora_fim) == None:
                                    hora_fim = input_por_voz()
                                    hora_fim_formatada = converter_horario(hora_fim)
                                    driver.find_element(By.NAME, "hora_fim").clear()
                                    driver.find_element(By.NAME, "hora_fim").send_keys(hora_fim_formatada)
                                else:
                                    hora_fim_formatada = converter_horario(hora_fim)
                                    driver.find_element(By.NAME, "hora_fim").clear()
                                    driver.find_element(By.NAME, "hora_fim").send_keys(hora_fim_formatada)
                                    
                            elif "descrição" in campo_alterar:
                                talk("Qual a nova descrição do evento?")
                                resposta = input_por_voz()
                                driver.find_element(By.NAME, "descricao").clear()
                                driver.find_element(By.NAME, "descricao").send_keys(resposta)
                                
                            elif "quantidade de vagas" in campo_alterar:
                                talk("Qual seria a nova quantidade de vagas para esse evento?")
                                resposta = input_por_voz()
                                driver.find_element(By.NAME, "quantidade_vagas").clear()
                                driver.find_element(By.NAME, "quantidade_vagas").send_keys(resposta)
                                
                       
                        else:
                            print("Resposta inválida. Tente novamente.")
                            talk("Resposta inválida. Tente novamente.")
                            
                else:
                    print("Campo inválido. Tente novamente.")
                    talk("Campo inválido. Tente novamente.")

                    
                        
            else:
                print("Usuario:", question)
                mensagens.append({"role": "user", "content": str(question)})

                answer = generate_answer(mensagens)

                print("Tito:", answer[0])

                if debug_custo:
                    print("Cost:\n", answer[1])

                mensagens.append({"role": "assistant", "content": answer[0]})

                if falar:
                    talk(answer[0])
        else:
            print("No message")
            continue

        if debugar:
            print("Mensagens", mensagens, type(mensagens))
    except sr.UnknownValueError:
            print("Ocorreu um erro no reconhecimento... Reiniciando")
            talk("Ocorreu um erro no reconhecimento... Reiniciando")
            continue
            
    except sr.RequestError:
            print("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
            talk("Desculpe, ocorreu um erro durante o reconhecimento de voz.")
            continue
            

print("Até Mais!")
