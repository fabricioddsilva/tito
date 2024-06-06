import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


# def agenda(nome, data, hora_inicio, hora_fim, desc):
#   start = str(data) + 'T' + str(hora_inicio) + ':00' + '-03:00'
#   end = str(data) + 'T' + str(hora_fim) + ':00' + '-03:00'
  
#Autenticação
creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
   
    with open("token.json", "w") as token:
      token.write(creds.to_json())

#Criar novo evento
try:
    service = build("calendar", "v3", credentials=creds)
    
    def event_body(nome, start, end, desc):
      event = {
        "summary": nome,
        "location": "https://g.co/kgs/ab9ERYn",
        "descripton": desc,
        "colorId": 1,
        "start" : {
          "dateTime": start,
          "timeZone": "America/Recife"
        },
        "end" : {
          "dateTime": end,
          "timeZone": "America/Recife"
        },
        "attendees": [
          {"email": "fabriciodsilva3404@gmail.com"},
        ]
        
      }
      return event


    def criar_evento(nome, data, hora_inicio, hora_fim, desc):
      
      start = str(data) + 'T' + str(hora_inicio) + ':00' + '-03:00'
      end = str(data) + 'T' + str(hora_fim) + ':00' + '-03:00'
      
      event = event_body(nome, start, end, desc)
      
      new_event = service.events().insert(calendarId = "primary", body = event).execute()
      return new_event.get('id')
    
    def editar_evento(nome, data, hora_inicio, hora_fim, desc, id):
      start = str(data) + 'T' + str(hora_inicio) + ':00' + '-03:00'
      end = str(data) + 'T' + str(hora_fim) + ':00' + '-03:00'
      
      event = event_body(nome, start, end, desc)
      try: 
        service.events().update(calendarId = "primary", eventId = id, body = event).execute()
        return 'ok'
      except HttpError as error:
        print(f"Ocorreu um erro: {error}")
    
    def excluir_evento(id):
      try:
        service.events().delete(calendarId = 'primary', eventId = id).execute()
        return 'ok'
      except HttpError as error:
        return error

except HttpError as error:
    print(f"An error occurred: {error}")
 



      
    
 


