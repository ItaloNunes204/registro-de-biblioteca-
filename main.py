from flask import Flask, render_template,redirect,session,request
from flask_session import Session
import banco as bd

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["POST", "GET"])
def login():
    if request.method == "POST":
        cnpj=request.form.get('cnpj')
        senha=request.form.get("senha")
        if bd.login(cnpj,senha) == True:
            session["name"] = cnpj
            return indexCliente()
        else:
            return render_template('login.html',saida='senha ou cnpj errados')
    else:
        return render_template('login.html',saida='')

@app.route("/cadastroBiblioteca",methods=["POST", "GET"])
def cadastroBiblioteca():
    if request.method == 'POST':
        nome = request.form.get('nome')
        responsavel = request.form.get('responsavel')
        cidade = request.form.get('cidade')
        cnpj = request.form.get('cnpj')
        senha = request.form.get('senha')
        if bd.mandaBiblioteca(nome,responsavel,cidade,cnpj,senha) == True:
            session["name"]=cnpj
            return indexCliente()
        else:
            return redirect(cadastroBiblioteca())
    else:
        return render_template("cadastroBiblioteca.html")

@app.route("/biblioteca")
def indexCliente():
    if not session.get('name'):
        return redirect('/login')
    else:
        return render_template('indexBiblioteca.html')

@app.route('/cadastroLivro', methods=["POST", "GET"])
def cadastroLivro():
    if not session.get('name'):
        return redirect('/login')
    else:
        if request.method == "POST":
            cnpj = session.get('name')
            nome = request.form.get("nome")
            autor = request.form.get("autor")
            editora = request.form.get("editora")
            codigo = request.form.get("codigo")
            tempo=request.form.get('tempo')
            if bd.mandaLivro(nome,autor,editora,codigo,cnpj,tempo) == True:
                return render_template("cadastroLivro.html", saida = 'cadastro realizado')
            else:
                return render_template("cadastroLivro.html", saida = 'erro no cadastro')
        else:
            return render_template("cadastroLivro.html",saida = '')

@app.route('/cadastroCliente',methods=['POST','GET'])
def cadastroCliente():
    if not session.get('name'):
        return redirect('/login')
    else:
        if request.method == 'POST':
            cnpj=session.get('name')
            cpf=request.form.get('cpf')
            nome=request.form.get('nome')
            senha=request.form.get('senha')
            if bd.buscaClienteCPF(cpf)==False:
                return render_template('cadastroUsuario.html', saida='ja cadastrado')
            else:
                if bd.mandaCliente(nome,cpf,senha,cnpj) == True:
                    return render_template('cadastroCliente.html',saida='CADASTRADO')
                else:
                    return render_template('cadastroCliente.html', saida='ERRO NO CADASTRO')
        else:
            return render_template('cadastroCliente.html',saida='')

@app.route('/listagemLivros/<mensagem>', methods=["POST", "GET"])
def listagemLivros(mensagem):
    if mensagem == None:
        mensagem=''
    if not session.get('name'):
        return redirect('/login')
    else:
        cnpj = session.get('name')
        if request.method == 'POST':
            nome=request.form.get('pesquisa')
            if nome == '':
                livros = bd.listaLivros(cnpj)
            else:
                livros=bd.buscaLivro(nome,cnpj)
            return render_template("listagemLivros.html",livros=livros,mensagem=mensagem)
        else:
            livros = bd.listaLivros(cnpj)
            return render_template("listagemLivros.html",livros=livros,mensagem=mensagem)

@app.route('/listagemCliente', methods=["POST", "GET"])
def listagemCliente():
    if not session.get('name'):
        return redirect('/login')
    else:
        cnpj = session.get('name')
        if request.method == "POST":
            pesquisa = request.form.get("pesquisa")
            if pesquisa =='':
                clientes = bd.listaClientes(cnpj)
                return render_template('listagemClientes.html', clientes=clientes)
            else:
                clientes = bd.buscaCliente(pesquisa,cnpj)
                return render_template('listagemClientes.html', clientes=clientes)
        else:
            clientes=bd.listaClientes(cnpj)
            return render_template('listagemClientes.html',clientes=clientes)

@app.route('/retiraPenalidade/<idCliente>', methods=["POST", "GET"])
def retiraPenalidade(idCliente):
    if not session.get('name'):
        return redirect('/login')
    else:
        if bd.aplicaPenalidade(idCliente,None) == True:
            return redirect('/listagemCliente')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

@app.route('/emprestimo/<id>', methods=["POST", "GET"])
def emprestimo(id):
    if not session.get('name'):
        return redirect('/login')
    else:
        cnpj = session.get('name')
        if request.method=='POST':
            idLivro = request.form.get('id')
            cpf = request.form.get('cpf')
            senha = request.form.get('senha')
            idCliente=bd.clienteConfirmacao(cpf,senha)
            if idCliente != False:
                if bd.criaRegistroEmprestimo(idLivro,idCliente,cnpj) == True:
                    return redirect('/listagemLivros/'+"emprestimo realizado")
                else:
                    return redirect('/listagemLivros/'+"erro no emprestimo")
            else:
                return redirect('/listagemLivros/'+"cpf ou senha errados verifique se o usuario esta penalizado")
        else:
            livro=bd.buscaLivroID(cnpj,id)
            return render_template('saidaEntrada.html',livro=livro[0],escolha='emprestimo')

@app.route('/devolucao/<id>', methods=["POST", "GET"])
def devolucao(id):
    if not session.get('name'):
        return redirect('/login')
    else:
        cnpj=session.get('name')
        if request.method == 'POST':
            idLivro = request.form.get('id')
            cpf = request.form.get('cpf')
            senha = request.form.get('senha')
            idCliente = bd.clienteConfirmacaoID(cpf,senha)
            if idCliente != False:
                if bd.registroDevolucao(idLivro,idCliente,cnpj)==True:
                    return redirect('/listagemLivros/'+"devolucao realizada")
                else:
                    return redirect('/listagemLivros/'+'erro na devolução')
            else:
                return redirect('/listagemLivros/'+'cpf ou senha errados')
        else:
            livro = bd.buscaLivroID(cnpj, id)
            return render_template('saidaEntrada.html', livro=livro[0], escolha='emprestimo')


if __name__ == "__main__":
    app.run(debug=True)