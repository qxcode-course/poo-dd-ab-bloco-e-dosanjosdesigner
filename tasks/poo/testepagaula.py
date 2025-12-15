from abc import ABC, abstractmethod

class MetodoPag(ABC):
    @abstractmethod
    def processar_pag(self, valor: float, desc: str):
        pass

class Pagamento:
    def __init__(self, valor: float, desc: str, metodo_pag: MetodoPag):
        self.valor: float = valor
        self.desc: str = desc
        self.metodo: MetodoPag = metodo_pag

    def resumo(self):
        print(f"Pagamento de R$ {self.valor}: {self.desc}")
    def validar_valor(self):
        if self.valor <= 0:
            raise ValueError("Valor invalido")
    
    def processar(self):
        self.validar_valor()
        self.resumo()
        self.metodo.processar_pag(self.valor, self.desc)

class MetodoPix(MetodoPag):
    def __init__(self, chave: str):
        self.chave: str = chave

    def get_chave(self):
        return self.chave

    def processar_pag(self, valor: float, desc: str):
        print(f"Pagando com pix chave {self.chave}, valor {valor}, produto {desc}")

def processar_pagamento(pag: Pagamento):
    pag.validar_valor()
    pag.resumo()
    pag.processar()

def MetodoCartao():
    def __init__(self, numero: str, titular: str, limite: float, bandeira: str = "Visa") :
        self.numero = numero
        self.titular = titular
        self. limite = limite
        self.bandeira = bandeira

def processar_pag(self, valor: float, desc: str):
    if valor > self.limite



metodoPix = MetodoPix("pagar@picpay.com")
metodoCartao = MetodoCartao("123123123", 500)
pagamento = Pagamento(desc="salgado", valor=5.90, metodo_pag=metodoPix)
pagamento.processar()

# ACOPLAMENTO
# dependencia baixa
# dependencia alta

# brincadeira da semana: Strategy patthern.  