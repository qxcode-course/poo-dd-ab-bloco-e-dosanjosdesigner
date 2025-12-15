from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, nome: str):
        self.nome = nome  
        

    def apresentar_nome(self) -> None:
        print(f"Eu sou um(a) {self.nome}!")

    @abstractmethod
    def fazer_som(self) -> None:
        """Deve imprimir o som característico do animal."""
        pass

    @abstractmethod
    def mover(self) -> None:
        """Deve imprimir como o animal se move."""
        pass



class Leao(Animal):
    def __init__(self, nome: str):
        super().__init__(nome)

    def fazer_som(self) -> None:
        print("Rugido: Rooooar!")

    def mover(self) -> None:
        print("O leão corre pelas savanas.")


class Elefante(Animal):
    def __init__(self, nome: str):
        super().__init__(nome)

    def fazer_som(self) -> None:
        print("Som: Trombar! Prrrrr!")

    def mover(self) -> None:
        print("O elefante caminha pesadamente.")


class Cobra(Animal):
    def __init__(self, nome: str):
        super().__init__(nome)

    def fazer_som(self) -> None:
        print("Som: Sssssss!")

    def mover(self) -> None:
        print("A cobra rasteja silenciosamente.")



def apresentar(animal: Animal) -> None:
    animal.apresentar_nome()
    animal.fazer_som()
    animal.mover()
    print(f"Tipo: {type(animal).__name__}")
    print("-" * 40)



if __name__ == "__main__":
    animais: list[Animal] = [
        Leao("Simba"),
        Elefante("Dumbo"),
        Cobra("Nagini"),
    ]

    for a in animais:
        apresentar(a)

    