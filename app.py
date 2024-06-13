import mysql.connector
from flask import Flask, request, render_template, redirect, url_for, session,json, jsonify
from dotenv import load_dotenv
import os
import agenda

load_dotenv()

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_SCHEMA')
)

# Inicializando o Flask
app = Flask(__name__, static_folder='static')

app.secret_key = os.getenv('SECRET_KEY')


# Endpoint para mostrar todos os eventos
@app.route('/', methods=['GET'])
def eventos():
    username = None

    #Verificando se a um usuário logado
    if 'username' in session:
        username = session['username']

    # Criação do cursor para executar comandos
    cursor = mydb.cursor()

  
    cursor.execute("SELECT * FROM eventos ORDER BY data_evento DESC")

    todos_eventos = cursor.fetchall()

    # Tratando os dados recebidos
    eventos = list()
    for evento in todos_eventos:
        eventos.append(
            {
                'id': evento[0],
                'nome': evento[1],
                'data': evento[2],
                'hora_inicio': evento[3],
                'hora_fim': evento[4],
                'descricao': evento[5],
                'vagas': evento[6]   
            }
        )

    # Terminado a execução do cursor
    cursor.close()

    # Renderizando o template em html e atribuindo os dados a variável eventos
    return render_template("eventos.html", username=username, eventos = eventos)


# Endpoint de criação de eventos
@app.route('/evento/novo', methods=['POST', 'GET'])
def form():
    username = None

    #Verificando se a um usuário logado
    if 'username' in session:
        username = session['username']
        
    # Caso a requisição for post
    if request.method == 'POST':

        req = request.get_json()

        google_event = agenda.criar_evento(req['nome'], req['data'], req['hora_inicio'], req['hora_fim'], req['descricao'])
        
        cursor = mydb.cursor()

        sql = f"INSERT INTO eventos (nome, data_evento, hora_inicio, hora_fim, descricao, qtd_visitantes, google_id) VALUES ('{req['nome']}','{req['data']}','{req['hora_inicio']}','{req['hora_fim']}', '{req['descricao']}','{req['visitantes']}','{google_event}')"

        cursor.execute(sql)

        mydb.commit()

        if (200):
            return "Evento Criado com Sucesso!!"

        return redirect(url_for('eventos'))

    return render_template("novo_evento.html")


#Editar Evento
@app.route("/editar/<id>", methods = ['GET', 'POST'])
def editar_evento(id):
    username = None

    #Verificando se a um usuário logado
    if 'username' in session:
        username = session['username']
        
    cursor = mydb.cursor()
    
    cursor.execute(f"SELECT nome, data_evento, hora_inicio, hora_fim, descricao, qtd_visitantes, google_id FROM eventos WHERE id = {id}")
    
    resultados = cursor.fetchall()
    
    evento = list()
    
    for resultado in resultados:
        evento.append(
            {
                "nome" : resultado[0],
                "data_evento" : resultado[1],
                "hora_inicio" : resultado[2],
                "hora_fim" : resultado[3],
                "descricao" : resultado[4],
                "visitantes" : resultado[5],
                "google_id" : resultado[6]
            }
        )
        
        if request.method == 'POST':
            req = request.json()
            evento_atualizado = agenda.editar_evento(req['nome'], req['data'], req['hora_inicio'], req['hora_fim'], req['descricao'], req['google_id'])
            cursor.execute(f"UPDATE eventos SET nome = '{req['nome']}', data_evento = '{req['data']}', hora_inicio = '{req['hora_inicio']}', hora_fim = '{req['hora_fim']}', descricao = '{req['descricao']}', qtd_visitantes = '{req['visitantes']}' WHERE id = '{id}' ")
            mydb.commit()
            if(200) and evento_atualizado == 'ok':
                return "Evento Alterado com Sucesso!!"
            else:
                render_template('editar_evento.html', msg = 'Não foi possível alterar o evento')
                
        return render_template('editar_evento.html', evento = evento, username = username)
 
#Deletar Evento   
@app.route('/deletar/<id>', methods=['GET','POST'])
def deletar_evento(id):
    
    if request.method == 'POST':
        req = request.json()
        
        cursor = mydb.cursor()
        cursor.execute(f"SELECT matricula FROM funcionarios WHERE matricula = '{req['matricula']}'")
        verificacao = cursor.fetchall()
        if verificacao == []:
            return render_template("verificacao.html", msg = 'Matrícula Inválida')
        else:
            cursor.execute(f"SELECT google_id FROM eventos WHERE id = {id}")
            resultados = cursor.fetchall()
            google_id = None
            for dado in resultados:
                google_id = dado[0]
            cursor.execute(f"DELETE FROM eventos WHERE id = {id}")
            evento_deletado = agenda.excluir_evento(google_id)
            mydb.commit()
            if (200) and evento_deletado == 'ok':
                return "Evento Deletado com Sucesso"
            else:
                return render_template("verificacao.html", msg = 'Ocorreu um erro durante a mudança')
        
            
    return render_template("verificacao.html")

# Endpoint de inscrição de visitantes recebendo o ID do evento
@app.route("/visitante/<id>", methods=['POST', 'GET'])
def visitante(id):
    username = None

    #Verificando se a um usuário logado
    if 'username' in session:
        username = session['username']

    # Caso a requisição for post, executa o processo de inscrição
    if request.method == 'POST':
        req = request.form

        cursor = mydb.cursor()

        cursor.execute(f"SELECT * FROM visitantes WHERE evento_id = {id}")

        resultados = cursor.fetchall()

        # Verificando no banco caso já exista o cpf cadastrado nessa visita
        for resultado in resultados:

            if req['cpf'] in resultado:

                # Caso o cpf já esteja cadastrado, renderiza o form.html com a mensagem
                return render_template("novo_visitante.html", msg='CPF já cadastrado nesse evento')

            # Caso o cpf não esteja cadastrado, executa a inscrição normalmente
            else:
                sql = f"INSERT INTO visitantes (nome, cpf, evento_id) VALUES ('{req['nome']}','{req['cpf']}','{id}')"
                cursor.execute(sql)
                mydb.commit()
                if (200):
                    print('Visitante adicionado com sucesso')
                    return redirect(url_for('eventos'))
                else:
                    return redirect(url_for('eventos'))

    # Renderiza o template com o formulário para inscrição
    return render_template("novo_visitante.html", username = username)


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = None

    #Verificando se a um usuário logado
    if 'username' in session:
        username = session['username']

    if request.method == 'POST':
        
        erro_validacao =  render_template("login.html", msg='Usuario, Senha ou Matricula Incorretos!!')    
    
        req = request.form

        cursor = mydb.cursor()

        cursor.execute(f"SELECT usuario, senha, matricula FROM funcionarios WHERE matricula = '{req['matricula']}'")

        resultado = cursor.fetchall()
        
        if resultado != [None]:
            for dado in resultado:
                if req['usuario'] in dado:
                    if req['senha'] in dado:
                        session['username'] = req['usuario']
                        return redirect(url_for('eventos'))
                    else:
                        return erro_validacao
                else:
                    return erro_validacao
    
    return render_template("login.html", username = username)

@app.route("/evento", methods = ['GET'])
def evento_proximo():
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM eventos ORDER BY data_evento DESC LIMIT 1")
    resultados = cursor.fetchall()
    evento = list()
    for dado in resultados:
        evento.append(
            {
                "id" : dado[0],
                "nome" : dado[1],
                "data_evento" : dado[2],
                "hora_inicio" : dado[3],
                "hora_fim" : dado[4],
                "visitantes" : dado[6]
            }
        )
    return jsonify(evento)

@app.route('/deslogar')
def logout():
    session.pop('username', None)
    return redirect(url_for('eventos'))


# Executando o aplicativo
if __name__ == '__main__':
    app.run()
