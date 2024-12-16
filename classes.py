class Funcionario:
    def __init__(self, email, senha) -> None:
        self.email = email
        self.senha = senha

class Cliente:
    def __init__(self, email, senha, saldo) -> None:
        self.email = email
        self.senha = senha
        self.saldo = saldo
    
    def deposito(self,valor):
        self.saldo += valor

    def retirada(self, valor):
        self.saldo -= valor

class Livro:
    def __init__(self, id_livro, titulo, autor, editora, ano_publicacao, isbn, genero, quantidade_total, quantidade_disponivel) -> None:
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano_publicacao = ano_publicacao
        self.isbn = isbn
        self.genero = genero
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = quantidade_disponivel
    
    def emprestimo(self):
        self.quantidade_disponivel -= 1
    
    def devolucao(self):
        self.quantidade_disponivel += 1

class Emprestimos:
    def __init__(self, id_emprestimo, id_livro, email_cliente, data_emprestimo, data_devolução, status) -> None:
        self.id_emprestimo = id_emprestimo
        self.id_livro = id_livro
        self.email_cliente = email_cliente
        self.data_emprestimo = data_emprestimo
        self.data_devolução = data_devolução
        self.status = status
    def devolver(self):
        self.status = "devolvido"

class Multas:
    def __init__(self, id_multa, id_cliente, valor, status, data_geracao, data_pagamento) -> None:
        self.id_multa = id_multa
        self.id_cliente = id_cliente
        self.valor = valor
        self.status = status
        self.data_geracao = data_geracao
        self.data_pagamento = data_pagamento
    def pagamento(self, data_pagamento):
        self.status = "pago"
        self.data_pagamento = data_pagamento
        