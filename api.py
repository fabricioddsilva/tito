from flask import Flask, request, json, jsonify
from datetime import datetime
import time
import mysql.connector
import os

os.environ["TZ"] = "America/Recife"
time.tzset()

db = mysql.connector.connect(
    host = "drakonor.mysql.pythonanywhere-services.com",
    user = "drakonor",
    password = "titoadmin",
    database = "drakonor$tito"
)

app = Flask(__name__)

@app.route("/auth", methods = ["POST"])
def autenticar():
    entrada = 0

    registro = datetime.now()

    req = request.json

    cursor = db.cursor()

    cursor.execute(f"SELECT uuid FROM funcionario WHERE uuid = '{req['uuid']}' ")

    resultado = cursor.fetchall()

    uuid = None

    for cartao in resultado:
        uuid = cartao[0]

    if uuid != None:
        entrada = 1
        cursor.execute(f"INSERT INTO log (registro, uuid, entrada) VALUES ('{registro}', '{uuid}', '{entrada}')")
        db.commit()
        return "Autenticado com Sucesso"
    else:
        cursor.execute(f"INSERT INTO log (registro, uuid, entrada) VALUES ('{registro}','{req['uuid']}', '{entrada}')")
        db.commit()
        return "Cartão não encontrado"

@app.route("/log", methods = ['GET'])
def log():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM log")
    resultado = cursor.fetchall()
    return jsonify(resultado)
