
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Union



class Valuable(ABC):
    @abstractmethod
    def getLabel(self) -> str:
        pass

    @abstractmethod
    def getValue(self) -> float:
        pass

    @abstractmethod
    def getVolume(self) -> int:
        pass

    def __str__(self) -> str:
       
        return self.getLabel()



class CoinType(Enum):
    
    M10  = ("M10",  0.10, 1)
    M25  = ("M25",  0.25, 2)
    M50  = ("M50",  0.50, 3)
    M100 = ("M100", 1.00, 4)

    def __init__(self, label: str, value: float, volume: int):
        self._label = label
        self._value = value
        self._volume = volume

    @property
    def label(self) -> str:
        return self._label

    @property
    def value(self) -> float:
        return self._value

    @property
    def volume(self) -> int:
        return self._volume


class Coin(Valuable):
    def __init__(self, ctype: CoinType):
        self.ctype = ctype

    def getLabel(self) -> str:
        return self.ctype.label

    def getValue(self) -> float:
        return self.ctype.value

    def getVolume(self) -> int:
        return self.ctype.volume

    def __str__(self) -> str:
        return f"{self.getLabel()}(R${self.getValue():.2f},V{self.getVolume()})"



class Item(Valuable):
    def __init__(self, label: str, volume: int, value: float):
        if volume <= 0:
            raise ValueError("volume do item deve ser positivo")
        if value < 0:
            raise ValueError("valor do item não pode ser negativo")
        self._label = label
        self._volume = int(volume)
        self._value = float(value)

    
    def getLabel(self) -> str:
        return self._label

    def getValue(self) -> float:
        return self._value

    def getVolume(self) -> int:
        return self._volume

    def setLabel(self, label: str) -> None:
        self._label = label

    def setVolume(self, volume: int) -> None:
        if volume <= 0:
            raise ValueError("volume do item deve ser positivo")
        self._volume = int(volume)

    def __str__(self) -> str:
        return f"{self._label}(R${self._value:.2f},V{self._volume})"



class Pig:
    def __init__(self, volumeMax: int):
        if volumeMax <= 0:
            raise ValueError("volume máximo deve ser positivo")
        self.broken: bool = False
        self.valuables: List[Valuable] = []
        self.volumeMax: int = int(volumeMax)

    
    def isBroken(self) -> bool:
        return self.broken

    def getVolumeMax(self) -> int:
        return self.volumeMax

   
    def getVolume(self) -> int:
        if self.broken:
            return 0
        return sum(v.getVolume() for v in self.valuables)

    
    def getValue(self) -> float:
        return sum(v.getValue() for v in self.valuables)

    
    def addValuable(self, valuable: Valuable) -> bool:
        """
        Insere moeda/item se o porco estiver inteiro e houver espaço de volume.
        Retorna True se inseriu; False caso não seja possível.
        """
        if self.broken:
            
            print("fail: porquinho quebrado, não pode inserir")
            return False
        novo_volume = self.getVolume() + valuable.getVolume()
        if novo_volume > self.volumeMax:
            print("fail: volume excedido")
            return False
        self.valuables.append(valuable)
        return True

    def breakPig(self) -> bool:
        """
        Quebra o porquinho. Após quebrar:
        - broken = True
        - getVolume() passa a retornar 0 (zerado)
        Os objetos permanecem armazenados para serem obtidos via getCoins/getItems.
        """
        if self.broken:
            print("fail: porquinho já está quebrado")
            return False
        self.broken = True
        return True

    def getCoins(self) -> List[Coin]:
        """
        Só pode obter quando quebrado.
        Retorna as moedas e as remove do porquinho.
        """
        if not self.broken:
            print("fail: porquinho inteiro, não pode obter")
            return []
        coins: List[Coin] = [v for v in self.valuables if isinstance(v, Coin)]
        
        self.valuables = [v for v in self.valuables if not isinstance(v, Coin)]
        return coins

    def getItems(self) -> List[Item]:
        """
        Só pode obter quando quebrado.
        Retorna os itens e os remove do porquinho.
        """
        if not self.broken:
            print("fail: porquinho inteiro, não pode obter")
            return []
        items: List[Item] = [v for v in self.valuables if isinstance(v, Item)]
       
        self.valuables = [v for v in self.valuables if not isinstance(v, Item)]
        return items

   
    def __str__(self) -> str:
        status = "broken" if self.broken else "intact"
        conteudo = ", ".join(str(v) for v in self.valuables) if self.valuables else "-"
        return (f"Pig({status}) vol={self.getVolume()}/{self.volumeMax} "
                f"val=R${self.getValue():.2f} contents=[{conteudo}]")
