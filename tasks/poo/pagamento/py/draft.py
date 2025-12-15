
from abc import ABC, abstractmethod

class Pagamento(ABC):
    def __init__(self, valor: float, descricao: str):
        self.valor = valor
        self.descricao = descricao

    def resumo(self) -> None:
        print(f"Pagamento de R$ {self.valor}: {self.descricao}")

    def validar_valor(self) -> None:
        if self.valor <= 0:
            raise ValueError("Valor inválido")

    @abstractmethod
    def processar(self) -> None:
        """Cada método de pagamento deve implementar sua lógica."""
        pass


class CartaoCredito(Pagamento):
    def __init__(self, valor: float, descricao: str, numero: str, nome_titular: str, limite_disponivel: float):
        super().__init__(valor, descricao)
        self.numero = numero
        self.nome_titular = nome_titular
        self.limite_disponivel = limite_disponivel

    def processar(self) -> None:
        if self.valor > self.limite_disponivel:
            
            raise ValueError(f"Limite insuficiente no cartão {self.numero}")
        
        self.limite_disponivel -= self.valor
        
        print(f"Pagamento aprovado no cartão {self.nome_titular}. Limite restante: {self.limite_disponivel:g}")


class Pix(Pagamento):
    def __init__(self, valor: float, descricao: str, chave: str, banco: str):
        super().__init__(valor, descricao)
        self.chave = chave
        self.banco = banco

    def processar(self) -> None:
       
        print(f"PIX enviado via {self.banco} usando chave {self.chave}")


class Boleto(Pagamento):
    def __init__(self, valor: float, descricao: str, codigo_barras: str, vencimento: str):
        super().__init__(valor, descricao)
        self.codigo_barras = codigo_barras
        self.vencimento = vencimento

    def processar(self) -> None:
        print("Boleto gerado. Aguardando pagamento...")



def processar_pagamento(pagamento: Pagamento) -> None:
    try:
        pagamento.validar_valor()
        pagamento.resumo()
        pagamento.processar()
        print()  
    except Exception as e:
        print(f"Erro: {e}")
        print()



if __name__ == "__main__":
    pagamentos: list[Pagamento] = [
        Pix(150, "Camisa esportiva", "email@ex.com", "Banco XPTO"),
        CartaoCredito(400, "Tênis esportivo", "1234 5678 9123 4567", "Cliente X", 500),
        Boleto(89.90, "Livro de Python", "123456789000", "2025-01-10"),
        CartaoCredito(800, "Notebook", "9999 8888 7777 6666", "Cliente Y", 700), 
    ]

    for pag in pagamentos:
        processar_pagamento(pag)
