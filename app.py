from flask import Flask,redirect,url_for,render_template,request
from flaskext.mysql import MySQL
from datetime import datetime

app=Flask(__name__)

#Conexão com MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'funcionarios'
mysql.init_app(app)


@app.route('/', methods=['GET','POST'])

def home():

    sql = "INSERT INTO `empregados` (`id`, `nome`, `email`, `foto`) VALUES (NULL, 'Amanda', 'amanda@gmail.com', 'fotoamanda.jpg'); "
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template('funcionarios/index.html')

#Essa rota chama o template Create.HTML
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
    return render_template('funcionarios/index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)