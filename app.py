from flask import Flask,redirect,url_for,render_template,request
from flaskext.mysql import MySQL

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
                                                                                #vai enviar nessa ordem
    sql = "INSERT INTO `empregados` (`id`, `nome`, `email`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    #na foto pego o filename por que tem outros parametros dela, por ex: tamanho e tipo JPG...
    #vai enviar nessa ordem
    dados =(_nome, _email, _foto.filename)

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, dados)
    conn.commit()
    return render_template('funcionarios/index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)