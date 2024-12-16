from flask import Flask, render_template, redirect, request, session, flash
import classes as cl
import banco as bd
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')
app.secret_key = "biblioteca"

#tela para a seleção de login
@app.route('/')
def index():
    return render_template("index.html")

#tela de login de funcionario 
@app.route("/login_funcionario", methods=["POST", "GET"])
def login_funcionario():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        funcionario = cl.Funcionario(email, senha)
        if bd.login_funcionario(funcionario) == True:
            session["name"] = email
            return redirect("/inicio_funci")
        else:
            return redirect("/login_funcionario")
    else:
        return render_template("login_funcionario.html")

#tela de login de cliente
@app.route("/login_cliente", methods=["POST", "GET"])
def login_cliente():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        cliente = cl.Cliente(email, senha, None)
        if bd.login_cliente(cliente) == True:
            session["name"] = email
            return redirect("/inicio_client")
        else:
            return redirect("/login_cliente")
    else:
        return render_template("login_cliente.html")

#tela de inicio do funcionario 
@app.route("/inicio_funci")
def inicio_funci():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        info = bd.get_funci(session.get("name"))
        return render_template("inicio_funci.html", info=info)

#tela de inicio do cliente
@app.route("/inicio_client")
def inicio_client():
    if not session.get("name"):
        return redirect('/login_cliente')
    else:
        info = bd.get_cliente(session.get("name"))
        return render_template("inicio_client.html", info=info)

#tela de cadastro de livro 
@app.route("/cadastro_livro", methods=["POST", "GET"])
def cadastro_livro():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        if request.method == "POST":
            titulo = request.form.get("titulo")
            autor = request.form.get("autor")
            editora = request.form.get("editora")
            ano_publicacao = str(request.form.get("ano_publicacao"))
            ano_publicacao = datetime.strptime(ano_publicacao, "%Y-%m-%d")
            ano_publicacao = ano_publicacao.strftime("%Y-%m-%d")
            isbn = request.form.get("isbn")
            genero = request.form.get("genero")
            quantidade_total = request.form.get("quantidade_total")
            livro = cl.Livro(None, titulo, autor, editora, ano_publicacao, isbn, genero, quantidade_total, quantidade_total)
            if bd.create_livro(livro) == True:
                return redirect("/inicio_funci")
            else:
                return redirect("/cadastro_livro")
        else:
            return render_template("cadastro_livro.html")

#tela de listagem de livros
@app.route("/listagem_livros", methods=["POST", "GET"])
def listagem_livro():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        livros = bd.get_livros()
        return render_template("lista_livros.html", livros = livros)

#tela de cadastro de emprestimo de livros
@app.route("/emprestimo/<id_livro>", methods=["POST", "GET"])
def emprestimo(id_livro):
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        if request.method == "POST":
            id_livro_emprestimo = request.form.get("id_livro")
            email_cliente = request.form.get("email")
            senha = request.form.get("senha")
            cliente = cl.Cliente(email_cliente, senha, None)
            if bd.login_cliente(cliente) == True:
                data = datetime.now()
                data = data.strftime("%Y-%m-%d")
                registo_emprestimo = cl.Emprestimos(None,id_livro_emprestimo,email_cliente,data,"NULL","emprestado")
                livro = bd.get_livro(id_livro_emprestimo)
                livro[0].emprestimo()
                if bd.create_empretimo(registo_emprestimo) == True and bd.modifica_livro(livro[0]):
                    return redirect("/inicio_funci")
                else:
                    return redirect("/listagem_livros")
        else:
            info = bd.get_livro(id_livro)
            return render_template("empretimo.html", livro = info[0])

# tela de listagem dos emprestimos 
@app.route("/listagem_emprestimo")
def listagem_emprestimo():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        emprestimos = bd.get_emprestimos()
        return render_template("listagem_emprestimo.html", emprestimos = emprestimos)

# tela para realizar as devoluções 
@app.route("/devolucao/<id_emprestimo>", methods=["POST", "GET"])
def devolucao(id_emprestimo):
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        if request.method == "POST":
            id_emprestimos = request.form.get("id_emprestimo")
            registro_emprestimo = bd.get_emprestimo(id_emprestimos)
            data = datetime.now()
            data = data.strftime("%Y-%m-%d")
            registro_emprestimo[0].devolver()
            registro_emprestimo[0].data_devolução = data
            livro = bd.get_livro(registro_emprestimo[0].id_livro)
            livro[0].devolucao()
            envio_banco = []
            envio_banco.append(bd.modifica_emprestimo(registro_emprestimo[0]))
            envio_banco.append(bd.modifica_livro(livro[0]))
            if envio_banco[0] == True and envio_banco[1] == True:
                data_prevista = registro_emprestimo[0].data_emprestimo + timedelta(days=-8)
                data_devolucao = datetime.now()
                data_devolucao = data_devolucao.date()
                devo = data_devolucao > data_prevista
                if  devo == True:
                    multa = cl.Multas(None,registro_emprestimo[0].email_cliente,20,"em aberto",data_devolucao,'NULL')
                    if bd.create_multas(multa):
                        return redirect("/inicio_funci")
                else:
                    return redirect("/inicio_funci")
            else:
                return redirect("/listagem_emprestimo")
        else:
            info = bd.get_emprestimo(id_emprestimo)
            return render_template("devolucao.html", emprestimo = info[0])

#teça para listagem de multas
@app.route("/listagem_multa_funci", methods=["POST", "GET"])
def listagem_multa():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        multas = bd.get_multas()
        return render_template("listagem_multa.html", multas = multas)

@app.route("/pagar_multa/<id_multa>", methods=["POST", "GET"])
def pagar_multa(id_multa):
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        if request.method == "POST":
            id_multas = request.form.get("id_multas")
            dados_multa = bd.get_multa(id_multas)
            data = datetime.now()
            data = data.strftime("%Y-%m-%d")
            dados_multa[0].pagamento(data)
            dados_cliente = bd.get_cliente(dados_multa[0].id_cliente)
            dados_cliente[0].retirada(dados_multa[0].valor)
            verificadores = []
            verificadores.append(bd.modifica_multa(dados_multa[0]))
            verificadores.append(bd.modifica_cliente(dados_cliente[0]))
            if verificadores[0] == True and verificadores[1] == True:
                return redirect("/inicio_funci")
            else:
                return redirect("/listagem_multa")
        else:
            multa = bd.get_multa(id_multa)
            multa = multa[0]
            cliente = bd.get_cliente(multa.id_cliente)
            cliente = cliente[0]
            return render_template("pagamento_multa.html",multa = multa, cliente = cliente)
        
#tela para realizar o deposito
@app.route("/deposito", methods=["POST", "GET"])
def deposito():
    if not session.get("name"):
        return redirect('/login_funcionario')
    else:
        if request.method == "POST":
            valor = request.form.get("valor")
            email_cliente = request.form.get("email")
            senha = request.form.get("senha")
            cliente = cl.Cliente(email_cliente, senha, None)
            if bd.login_cliente(cliente) == True:
                cliente = bd.get_cliente(cliente.email)
                cliente[0].deposito(float(valor))
                verificador = bd.modifica_cliente(cliente[0])
                if verificador == True:
                    return redirect("/inicio_funci")
                else:
                    return redirect("/deposito")
            else:
                return redirect("/deposito")
        else:
            return render_template("deposito.html")

#tela para realizar a listagem de emprestimos         
@app.route("/listagem_emprestimos_cliente")
def listagem_emprestimos_cliente():
    if not session.get("name"):
        return redirect('/inicio_client')
    else:
        emprestimos = bd.get_emprestimos_cliente(session.get("name"))
        return render_template("listagem_emprestimo_cliente.html", emprestimos = emprestimos)

# tela para realizar a listagem das multas
@app.route("/listagem_multas")
def listagem_multas():
    if not session.get("name"):
        return redirect('/inicio_client')
    else:
        multas = bd.get_multas_email(session.get("name"))
        return render_template("listagem_multa_cliente.html", multas = multas)

@app.route("/pagar_multa_cliente/<id_multa>", methods=["POST", "GET"])
def pagar_multa_cliente(id_multa):
    if not session.get("name"):
        return redirect('/inicio_client')
    else:
        if request.method == "POST":
            id_multas = request.form.get("id_multas")
            dados_multa = bd.get_multa(id_multas)
            data = datetime.now()
            data = data.strftime("%Y-%m-%d")
            dados_multa[0].pagamento(data)
            dados_cliente = bd.get_cliente(dados_multa[0].id_cliente)
            dados_cliente[0].retirada(dados_multa[0].valor)
            verificadores = []
            verificadores.append(bd.modifica_multa(dados_multa[0]))
            verificadores.append(bd.modifica_cliente(dados_cliente[0]))
            if verificadores[0] == True and verificadores[1] == True:
                return redirect("/inicio_client")
            else:
                return redirect("/listagem_multa_cliente")
        else:
            multa = bd.get_multa(id_multa)
            multa = multa[0]
            cliente = bd.get_cliente(multa.id_cliente)
            cliente = cliente[0]
            return render_template("pagamento_multa.html",multa = multa, cliente = cliente)

#função para realizar a saida
@app.route("/sair")
def sair():
    session["name"] = None
    return redirect("/")

if __name__ == "__name__":
    app.run(debug=True)
