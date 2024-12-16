import classes
import mysql.connector
from mysql.connector import Error


# conectando ao banco
try:
    con = mysql.connector.connect(host='localhost', database='biblioteca', user='root', password='italo175933')
    cursor = con.cursor()
    conexao = True
except Error as erro:
    print("Erro ao se conectar ao banco de dados: {}".format(erro))
    conexao = False

def login_funcionario(funcionario):
    comando = ("SELECT * FROM biblioteca.funcinario WHERE email = \'{}\' and senha = \'{}\'".format(funcionario.email, funcionario.senha))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = True
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def login_cliente(cliente):
    comando = ("SELECT * FROM biblioteca.cliente WHERE email = \'{}\' and senha = \'{}\'".format(cliente.email, cliente.senha))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = True
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def create_livro(livro):
    comando = ("INSERT INTO biblioteca.livro (titulo, autor, editora, ano_publicacao, isbn, genero,quantidade_total, quantidade_disponivel)"
               "VALUE(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})".format(livro.titulo, livro.autor, livro.editora, livro.ano_publicacao, livro.isbn, livro.genero, livro.quantidade_total, livro.quantidade_disponivel))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("erro ao criar livro: {}".format(e))
        saida = False
    return saida

def get_livros():
    comando = ("SELECT * FROM biblioteca.livro")
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Livro(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
            saida = lista
    except Error as e:
        print("Erro ao realizar a busca: {}".format(e))
        saida = "Erro"
    return saida

def get_livro(id):
    comando = ("SELECT * FROM biblioteca.livro WHERE id_livro = \'{}\'".format(id))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Livro(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
            saida = lista
    except Error as e:
        print("Erro ao realizar a busca: {}".format(e))
        saida = "Erro"
    return saida

def modifica_livro(livro):
    comando = ("UPDATE biblioteca.livro SET titulo = \'{}\', autor = \'{}\', editora = \'{}\', ano_publicacao = \'{}\', isbn = \'{}\', genero = \'{}\',quantidade_total = {}, quantidade_disponivel = {} WHERE id_livro = \'{}\'".format(livro.titulo, livro.autor, livro.editora, livro.ano_publicacao, livro.isbn, livro.genero, livro.quantidade_total, livro.quantidade_disponivel, livro.id_livro))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("Erro ao modificar: {}".format(e))
        saida = False
    return saida

def create_empretimo(emprestimo):
    comando = ("INSERT INTO biblioteca.emprestimo(id_livro, email_cliente, data_emprestimo, data_devolução, statuss)"
               "VALUE({},\'{}\',\'{}\',{},\'{}\')".format(emprestimo.id_livro, emprestimo.email_cliente, emprestimo.data_emprestimo, emprestimo.data_devolução, emprestimo.status))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("erro ao criar conta: {}".format(e))
        saida = False
    return saida

def modifica_emprestimo(emprestimo):
    comando = ("UPDATE biblioteca.emprestimo SET id_livro = \'{}\', email_cliente = \'{}\', data_emprestimo = \'{}\', data_devolução = \'{}\', statuss = \'{}\' WHERE id_emprestimo = {}".format(emprestimo.id_livro, emprestimo.email_cliente, emprestimo.data_emprestimo, emprestimo.data_devolução, emprestimo.status, emprestimo.id_emprestimo))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("Erro ao modificar: {}".format(e))
        saida = False
    return saida

def get_emprestimos():
    comando = ("SELECT * FROM biblioteca.emprestimo")
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Emprestimos(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5]))
            saida = lista
    except Error as e:
        print("Erro ao realizar a busca: {}".format(e))
        saida = "Erro"
    return saida

def get_emprestimo(id_emprestimo):
    comando = ("SELECT * FROM biblioteca.emprestimo WHERE id_emprestimo = \'{}\'".format(id_emprestimo))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Emprestimos(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5]))
            saida = lista
    except Error as e:
        print("Erro ao realizar a busca: {}".format(e))
        saida = "Erro"
    return saida

def get_clientes():
    comando = ("SELECT * FROM biblioteca.cliente")
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Cliente(linha[0],linha[1],linha[2]))
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def get_cliente(email):
    comando = ("SELECT * FROM biblioteca.cliente WHERE email = \'{}\'".format(email))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Cliente(linha[0],linha[1],linha[2]))
            saida = lista
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def modifica_cliente(cliente):
    comando = ("UPDATE biblioteca.cliente SET senha = \'{}\', saldo = \'{}\' WHERE email = \'{}\'".format(cliente.senha, cliente.saldo, cliente.email))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("Erro ao modificar: {}".format(e))
        saida = False
    return saida

def get_emprestimos_cliente(email):
    comando = ("SELECT * FROM biblioteca.emprestimo WHERE email_cliente = \'{}\'".format(email))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            lista = []
            for linha in linhas:
                lista.append(classes.Emprestimos(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5]))
            saida = lista
    except Error as e:
        print("Erro ao realizar a busca: {}".format(e))
        saida = "Erro"
    return saida

def get_multas():
    comando = ("SELECT * FROM biblioteca.multa")
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = []
            for linha in linhas:
                saida.append(classes.Multas(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5]))
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def get_multas_email(email):
    comando = ("SELECT * FROM biblioteca.multa WHERE id_cliente = \'{}\'".format(email))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = []
            for linha in linhas:
                saida.append(classes.Multas(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5]))
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def create_multas(multas):
    comando = ("INSERT INTO biblioteca.multa (id_cliente, valor, statuss, data_geracao, data_pagamento)"
               "VALUE(\'{}\',\'{}\',\'{}\',\'{}\',{})".format(multas.id_cliente, multas.valor, multas.status, multas.data_geracao, multas.data_pagamento))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("erro ao criar conta: {}".format(e))
        saida = False
    return saida

def get_multa(id_multa):
    comando = ("SELECT * FROM biblioteca.multa WHERE id_multa = \'{}\'".format(id_multa))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = []
            for linha in linhas:
                saida.append(classes.Multas(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5]))
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def modifica_multa(multa):
    comando = ("UPDATE biblioteca.multa SET id_cliente = \'{}\', valor = \'{}\', statuss = \'{}\', data_geracao = \'{}\', data_pagamento = \'{}\' WHERE id_multa = \'{}\'".format(multa.id_cliente, multa.valor, multa.status, multa.data_geracao, multa.data_pagamento, multa.id_multa))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("Erro ao modificar: {}".format(e))
        saida = False
    return saida

def get_funci(email):
    comando = ("SELECT * FROM biblioteca.funcinario WHERE email = \'{}\'".format(email))
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = []
            for linha in linhas:
                saida.append(classes.Funcionario(linha[0],linha[1]))
    except Error as e:
        print("Erro ao realizar o login: {}".format(e))
        saida = "Erro"
    return saida

def create_cliente(cliente):
    comando = ("INSERT INTO biblioteca.cliente (email, senha, saldo)"
               "VALUE(\'{}\',\'{}\',\'{}\')".format(cliente.email, cliente.senha, cliente.saldo))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("erro ao criar conta: {}".format(e))
        saida = False
    return saida

def create_funcionario(funcionario):
    comando = ("INSERT INTO biblioteca.funcinario (email, senha)"
               "VALUE(\'{}\',\'{}\')".format(funcionario.email, funcionario.senha))
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        print("erro ao criar conta: {}".format(e))
        saida = False
    return saida
