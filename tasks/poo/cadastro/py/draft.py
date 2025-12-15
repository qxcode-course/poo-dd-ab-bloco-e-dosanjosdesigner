
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List



class Account(ABC):
    def __init__(self, accId: int, clientId: str, typeId: str):
        self._accId = accId
        self._clientId = clientId
        self._typeId = typeId
        self._balance: float = 0.0

    
    def deposit(self, value: float) -> None:
        if value <= 0:
            raise ValueError("fail: valor de depósito deve ser positivo")
        self._balance += value

    def withdraw(self, value: float) -> None:
        if value <= 0:
            raise ValueError("fail: valor de saque deve ser positivo")
        
        if self._balance < value:
            raise ValueError("fail: saldo insuficiente")
        self._balance -= value

    def transfer(self, other: "Account", value: float) -> None:
        if other is None:
            raise ValueError("fail: conta destino inexistente")
        self.withdraw(value)
        other.deposit(value)

    
    @abstractmethod
    def updateMonthly(self) -> None:
        """Aplica a regra mensal específica da conta."""
        pass

     
    def getBalance(self) -> float:
        return self._balance

    def getId(self) -> int:
        return self._accId

    def getClientId(self) -> str:
        return self._clientId

    def getTypeId(self) -> str:
        return self._typeId

    def __str__(self) -> str:
        return f"{self._typeId}:{self._accId}:{self._clientId}:{self._balance:.2f}"



class CheckingAccount(Account):
    monthlyFee: float = 20.0  

    def __init__(self, accId: int, clientId: str):
        super().__init__(accId, clientId, "CC")

    def updateMonthly(self) -> None:
        
        self._balance -= self.monthlyFee



class SavingsAccount(Account):
    monthlyInterest: float = 0.01  # 1%

    def __init__(self, accId: int, clientId: str):
        super().__init__(accId, clientId, "PP")

    def updateMonthly(self) -> None:
        
        self._balance *= (1.0 + self.monthlyInterest)



class Client:
    def __init__(self, name: str, clientId: str):
        self._name = name
        self._clientId = clientId
        self._accounts: List[Account] = []

    def addAccount(self, acc: Account) -> None:
        self._accounts.append(acc)

    def getAccounts(self) -> List[Account]:
        return list(self._accounts)

    def getClientId(self) -> str:
        return self._clientId

    def __str__(self) -> str:
        accs = " ".join(str(a) for a in self._accounts) if self._accounts else "-"
        return f"{self._clientId}:{self._name} [{accs}]"



class Agency:
    def __init__(self):
        self.accounts: Dict[int, Account] = {}  
        self.clients: Dict[str, Client] = {}    
        self.nextAccountId: int = 1

    def getAccount(self, accountId: int) -> Account | None:
        return self.accounts.get(accountId)

    def addClient(self, clientId: str, name: str) -> None:
        if clientId in self.clients:
            raise ValueError("fail: cliente já existe")
        
        client = Client(name, clientId)
        self.clients[clientId] = client

        
        cc = CheckingAccount(self.nextAccountId, clientId)
        self.nextAccountId += 1
        pp = SavingsAccount(self.nextAccountId, clientId)
        self.nextAccountId += 1

        
        self.accounts[cc.getId()] = cc
        self.accounts[pp.getId()] = pp
        client.addAccount(cc)
        client.addAccount(pp)

   
    def deposit(self, accId: int, value: float) -> None:
        acc = self.getAccount(accId)
        if acc is None:
            raise ValueError("fail: conta inexistente")
        acc.deposit(value)

    def withdraw(self, accId: int, value: float) -> None:
        acc = self.getAccount(accId)
        if acc is None:
            raise ValueError("fail: conta inexistente")
        acc.withdraw(value)

    def transfer(self, fromAccId: int, toAccId: int, value: float) -> None:
        src = self.getAccount(fromAccId)
        dst = self.getAccount(toAccId)
        if src is None or dst is None:
            raise ValueError("fail: conta inexistente")
        src.transfer(dst, value)

    def updateMonthly(self) -> None:
        
        for acc in self.accounts.values():
            acc.updateMonthly()

    def __str__(self) -> str:
        
        cls = " | ".join(str(c) for c in self.clients.values()) or "-"
        
        accs = " ".join(str(a) for a in self.accounts.values()) or "-"
        return f"Clientes: {cls}\nContas: {accs}"
