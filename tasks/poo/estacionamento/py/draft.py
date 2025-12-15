
from abc import ABC, abstractmethod


class Veiculo(ABC):
    def __init__(self, id: str, tipo: str):
        self._id = id
        self._tipo = tipo
        self._horaEntrada: int | None = None  

    
    def setEntrada(self, horaEntrada: int) -> None:
        self._horaEntrada = int(horaEntrada)

    def getEntrada(self) -> int | None:
        return self._horaEntrada

    def getId(self) -> str:
        return self._id

    def getTipo(self) -> str:
        return self._tipo

    @abstractmethod
    def calcularValor(self, horaSaida: int) -> float:
        """Calcula o valor com base no tempo (minutos) e regras de cada tipo."""
        pass

    def __str__(self) -> str:
        ent = self._horaEntrada if self._horaEntrada is not None else "-"
        return f"{self._tipo}:{self._id} entrou={ent}"



class Bike(Veiculo):
    def __init__(self, id: str):
        super().__init__(id, "bike")

    def calcularValor(self, horaSaida: int) -> float:
        if self._horaEntrada is None:
            raise ValueError("Veículo sem hora de entrada")
        
        return 3.0


class Moto(Veiculo):
    def __init__(self, id: str):
        super().__init__(id, "moto")

    def calcularValor(self, horaSaida: int) -> float:
        if self._horaEntrada is None:
            raise ValueError("Veículo sem hora de entrada")
        minutos = max(0, int(horaSaida) - int(self._horaEntrada))
        return minutos / 20.0


class Carro(Veiculo):
    def __init__(self, id: str):
        super().__init__(id, "carro")

    def calcularValor(self, horaSaida: int) -> float:
        if self._horaEntrada is None:
            raise ValueError("Veículo sem hora de entrada")
        minutos = max(0, int(horaSaida) - int(self._horaEntrada))
        valor = minutos / 10.0
        return max(5.0, valor)  



class Estacionamento:
    def __init__(self):
        self.veiculos: list[Veiculo] = []
        self.horaAtual: int = 0  

    
    def procurarVeiculo(self, id: str) -> int:
        for i, v in enumerate(self.veiculos):
            if v.getId() == id:
                return i
        return -1

    
    def estacionar(self, veiculo: Veiculo) -> None:
        if self.procurarVeiculo(veiculo.getId()) != -1:
            print("fail: veículo já está estacionado")
            return
        veiculo.setEntrada(self.horaAtual)
        self.veiculos.append(veiculo)

   
    def pagar(self, id: str) -> None:
        idx = self.procurarVeiculo(id)
        if idx == -1:
            print("fail: veículo inexistente")
            return
        v = self.veiculos[idx]
        try:
            valor = v.calcularValor(self.horaAtual)
            print(f"valor a pagar ({v.getTipo()} {v.getId()}): R$ {valor:.2f}")
        except Exception as e:
            print(f"fail: {e}")

    
    def sair(self, id: str) -> None:
        idx = self.procurarVeiculo(id)
        if idx == -1:
            print("fail: veículo inexistente")
            return
        v = self.veiculos[idx]
        try:
            valor = v.calcularValor(self.horaAtual)
            print(f"{v.getTipo()} {v.getId()} pagou R$ {valor:.2f} e saiu")
          
            self.veiculos.pop(idx)
        except Exception as e:
            print(f"fail: {e}")

    
    def passarTempo(self, tempo: int) -> None:
        if tempo < 0:
            print("fail: tempo negativo")
            return
        self.horaAtual += int(tempo)

    def __str__(self) -> str:
        lista = ", ".join(str(v) for v in self.veiculos) if self.veiculos else ""
        return f"hora={self.horaAtual} min\nveiculos: [{lista}]"



def main():
    est = Estacionamento()
    print("Comandos:")
    print("  in tipo id        -> entra veículo (tipo: bike|moto|carro)")
    print("  pass m            -> avança m minutos")
    print("  pay id            -> mostra valor a pagar agora")
    print("  out id            -> calcula, cobra e remove veículo")
    print("  show              -> mostra estado")
    print("  end               -> encerra")
    print("-" * 60)

    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        try:
            if cmd == "in" and len(parts) == 3:
                tipo, vid = parts[1], parts[2]
                if tipo == "bike":
                    est.estacionar(Bike(vid))
                elif tipo == "moto":
                    est.estacionar(Moto(vid))
                elif tipo == "carro":
                    est.estacionar(Carro(vid))
                else:
                    print("fail: tipo inválido")

            elif cmd == "pass" and len(parts) == 2:
                est.passarTempo(int(parts[1]))

            elif cmd == "pay" and len(parts) == 2:
                est.pagar(parts[1])

            elif cmd == "out" and len(parts) == 2:
                est.sair(parts[1])

            elif cmd == "show" and len(parts) == 1:
                print(est)

            elif cmd == "end":
                break

            else:
                print("fail: comando inválido")
        except Exception as e:
            print(f"fail: {e}")


if __name__ == "__main__":
    main()
