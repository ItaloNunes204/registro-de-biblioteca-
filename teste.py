import classes as cl
import banco as bd 

def cria_cliente():
    i = 0
    while i < 100:
        email = "teste{}.outlook.com".format(i)
        senha = "12345"
        saldo = 100*i
        cliente = cl.Cliente(email,senha,saldo)
        if bd.create_cliente(cliente) == True:
            print(True)
        else:
            print(False)
        i+=1
def cria_funcionario():
    i = 0
    while i < 100:
        email = "teste{}.outlook.com".format(i)
        senha = "12345"
        cliente = cl.Funcionario(email,senha,)
        if bd.create_cliente(cliente) == True:
            print(True)
        else:
            print(False)
        i+=1
