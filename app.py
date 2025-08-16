from flask import Flask,redirect,url_for,render_template,request
from flaskext.mysql import MySQL
from datetime import datetime
import os #múdulo  do sistema operacional p/ buscar a foto

app=Flask(__name__)

#Conexão com MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'funcionarios'
mysql.init_app(app)

#Para mostrar a foto
PASTA = os.path.join('uploads')
app.config['PASTA'] = PASTA


@app.route('/', methods=['GET','POST'])

def home():

    sql = "SELECT * FROM `empregados`;"
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    #Para selecionar as infos do banco
    funcionarios = cursor.fetchall()
    print(funcionarios) #agora atualizando a index já mostra no vscode

    conn.commit()                                      #Essa variavel é a do print(funcionarios) que recebeu os dados
    return render_template('funcionarios/index.html', funcionarios=funcionarios)

#Rota para Excluir, delete
@app.route('/delete/<int:id>')
def delete(id):

    #Conectar com banco
    conn = mysql.connect()
    cursor=conn.cursor()

   #Para excluir imagem foto da PASTA
    cursor.execute("SELECT foto FROM empregados WHERE id = %s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['PASTA'], fila[0][0]))
    
    cursor.execute("DELETE FROM empregados WHERE id=%s",(id))
    conn.commit();
    return redirect('/')

#Rota para Editar, edit
@app.route('/edit/<int:id>')
def edit(id):

    #Conecta com banco
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empregados WHERE id=%s",(id))

    #Para selecionar dados do banco
    funcionarios = cursor.fetchall()
    print(funcionarios)
    return render_template('funcionarios/edit.html', funcionarios=funcionarios)

#Rota para Update
@app.route('/update', methods=['POST'])
def update():

    #variaveis que receberão dados p/ Atualizar
    _nome = request.form['txtNome']
    _email = request.form['txtEmail']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    sql = "UPDATE empregados SET nome = %s, email = %s WHERE id = %s;"
    
    #vai enviar nessa ordem
    dados = (_nome, _email, id)

    conn = mysql.connect()
    cursor=conn.cursor()

     #Criar tempo agora e variavel tempo para novo nome da foto
    now = datetime.now()
    tempo = now.strftime("%Y%H%M%S") #Ano - Hora - Mes - Segundo
    if _foto.filename != '':
        #variavel de novo nome da foto
        novo_nomeFoto = tempo + _foto.filename
        #salva na pasta uploads
        _foto.save("uploads/" + novo_nomeFoto)

        cursor.execute("SELECT foto FROM empregados WHERE id = %s", id)
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['PASTA'], fila[0][0]))
        cursor.execute("UPDATE empregados SET foto = %s WHERE id = %s", (novo_nomeFoto, id))
        conn.commit()
                   
    cursor.execute(sql, dados)               
    conn.commit()

    return redirect('/')

#Rota / chama o template Create.HTML
@app.route('/create')
def create():
    return render_template('funcionarios/create.html')

    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('funcionarios/index.html')

#Rota para enviar dados do create action = store
@app.route('/store', methods=['POST'])
def storage():

    #variaveis:
    _nome = request.form['txtNome']
    _email = request.form['txtEmail']
    _foto = request.files['txtFoto']

    #Criar tempo agora e variavel tempo para novo nome da foto
    now = datetime.now()
    tempo = now.strftime("%Y%H%M%S") #Ano - Hora - Mes - Segundo

    if _foto.filename != '':
        #variavel de novo nome da foto
        novo_nomeFoto = tempo + _foto.filename
        #salva na pasta uploads
        _foto.save("uploads/" + novo_nomeFoto)

                                                                                #vai enviar nessa ordem
    sql = "INSERT INTO `empregados` (`id`, `nome`, `email`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    #na foto pego o filename por que tem outros parametros dela, por ex: tamanho e tipo JPG...
    #vai enviar nessa ordem
    dados =(_nome, _email, novo_nomeFoto) #novo nome da foto

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, dados)
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)