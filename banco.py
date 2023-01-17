import mysql.connector
from mysql.connector import Error
import datetime

try:
    con = mysql.connector.connect(host='localhost', database='biblioteca', user='root', password='italo175933')
    cursor = con.cursor()
    conexao=True
except:
    conexao = False

#-----------------------cadastro e busca--------------------------------

def mandaBiblioteca(nome,responsavel,cidade,cnpj,senha):
    comando = """ INSERT INTO biblioteca.biblioteca(nome,responsavel,cidade,cnpj,senha) 
            VALUE (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(nome,responsavel,cidade,cnpj,senha)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def login(cnpj,senha):
    comando = "SELECT*FROM biblioteca.biblioteca WHERE cnpj=\'{}\' and senha=\'{}\'".format(cnpj,senha)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return True
    except Error as e:
        return False

def mandaLivro(nome,autor,editora,codigo,cnpj,tempo):
    comando =  """INSERT INTO biblioteca.livro(codigo,nome,situacao,cnpj,autor,editora,tempo)
                VALUE (\'{}\',\'{}\',True,\'{}\',\'{}\',\'{}\',{})""".format(codigo,nome,cnpj,autor,editora,tempo)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def mandaCliente(nome,cpf,senha,cnpj):
    comando = """INSERT INTO biblioteca.cliente(nome,cpf,senha,cidade,situacao,cnpj) 
    VALUE (\'{}\',\'{}\',\'{}\',\'{}\',True,\'{}\')""".format(nome,cpf,senha,buscaCidade(cnpj),cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def listaLivros(cnpj):
    comando = "SELECT*FROM biblioteca.livro WHERE cnpj=\'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False

def buscaLivro(nome,cnpj):
    comando = "SELECT*FROM biblioteca.livro WHERE nome =\'{}\' and cnpj=\'{}\'".format(nome,cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False

def listaClientes(cnpj):
    comando = "SELECT*FROM biblioteca.cliente WHERE cnpj=\'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False

def buscaCliente(nome,cnpj):
    comando = "SELECT*FROM biblioteca.cliente WHERE nome =\'{}\' and cnpj=\'{}\'".format(nome, cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False

def buscaClienteCPF(cpf):
    comando = "SELECT*FROM biblioteca.cliente WHERE cpf =\'{}\'".format(cpf)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return True
        else:
            return False
    except Error as e:
        return False

#----------------------entrada e saida de livro---------------------------------

def criaRegistroEmprestimo(idLivro,idCliente,cnpj):
    comando = """ INSERT INTO biblioteca.emprestimo(situacao,idLivro,idCliente,emprestimo,devolucao,cnpj) 
                VALUE (False,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')""".format(idLivro,idCliente,pegaTempoAtual(),calculaTempo(idLivro),cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
        situacaoCliente(idCliente,False)
        situacaoLivro(idLivro,False)
    except Error as e:
        saida = False
    return saida

def registroDevolucao(idLivro,idCliente,cnpj):
    comando = " UPDATE biblioteca.emprestimo set situacao = True where idLivro = \'{}\' and situacao = False ".format(idLivro)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
        verificaPenalidade(idLivro,cnpj,idCliente)
        situacaoCliente(idCliente,True)
        situacaoLivro(idLivro,True)
    except Error as e:
        saida = False
    return saida

def situacaoCliente(idCliente,situacao):
    comando = " UPDATE biblioteca.cliente set situacao = {} where id=\'{}\' ".format(situacao,idCliente)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def situacaoLivro(idLivro,situacao):
    comando = " UPDATE biblioteca.livro set situacao = {} where id=\'{}\' ".format(situacao,idLivro)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

#-------------------------penalidade e verificação de cliente------------------------------

def verificaPenalidade(idLivro,cnpj,idCliente):
    comando = "SELECT devolucao FROM biblioteca.emprestimo WHERE id =\'{}\' and cnpj=\'{}\'".format(idLivro, cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = linhas[0][0]
            if comparaDatas(saida) == 'atrasado':
                aplicaPenalidade(idCliente,dataPenalidade())
            else:
                pass
            saida=True
    except Error as e:
        saida = False
    return saida

def aplicaPenalidade(idCliente,penalidade):
    comando = " UPDATE biblioteca.cliente set penalidade = {} where id=\'{}\' ".format(penalidade,idCliente)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def clienteConfirmacao(cpf,senha):
    comando = "SELECT id FROM biblioteca.cliente WHERE cpf =\'{}\' and senha=\'{}\' and situacao = 1".format(cpf,senha)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas[0][0]
    except Error as e:
        return False

def clienteConfirmacaoID(cpf,senha):
    comando = "SELECT id FROM biblioteca.cliente WHERE cpf =\'{}\' and senha=\'{}\' and situacao = 0".format(cpf, senha)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas[0][0]
    except Error as e:
        return False

#---------------------------------------------------------------------------------------------

def buscaCidade(cnpj):
    comando = "SELECT cidade FROM biblioteca.biblioteca WHERE cnpj=\'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = linhas[0][0]
    except Error as e:
        saida = False
    return saida

def pegaTempoAtual():
    tempo=datetime.datetime.now().date()
    return tempo

def calculaTempo(id):
    tempo = buscaTempoLivro(id)
    diaEntrada = datetime.datetime.now().date()
    saida=diaEntrada + datetime.timedelta(days=tempo)
    return saida

def dataPenalidade():
    penalidade = pegaTempoAtual() + datetime.timedelta(days=7)
    return penalidade

def comparaDatas(dataEsperada):
    if dataEsperada > pegaTempoAtual():
        saida = 'em dia'
    else:
        if dataEsperada == pegaTempoAtual():
            saida = 'em dia'
        else:
            saida = 'atrasado'
    return saida

def buscaTempoLivro(id):
        comando = "SELECT tempo FROM biblioteca.livro WHERE id=\'{}\'".format(id)
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            if len(linhas) == 0:
                saida = False
            else:
                saida = linhas[0][0]
        except Error as e:
            saida = False
        return saida

def buscaLivroID(cnpj,id):
    comando = "SELECT*FROM biblioteca.livro WHERE id =\'{}\' and cnpj=\'{}\'".format(id, cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False