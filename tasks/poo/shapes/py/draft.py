
from abc import ABC, abstractmethod
from math import pi, hypot

# ===== Interface / Classe Abstrata =====
class Shape(ABC):
    @abstractmethod
    def getArea(self) -> float:
        pass

    @abstractmethod
    def getPerimeter(self) -> float:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

    # Opcional (aparece no diagrama): verificar se um ponto está dentro da forma
    def inside(self, point: "Point2D") -> bool:
        raise NotImplementedError("inside() não implementado para esta forma")


# ===== Classe Point2D =====
class Point2D:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"


# ===== Classe Circle =====
class Circle(Shape):
    def __init__(self, center: Point2D, radius: float):
        if radius <= 0:
            raise ValueError("Raio deve ser positivo")
        self.name = "Circ"
        self.center = center
        self.radius = float(radius)

    def getName(self) -> str:
        return self.name

    def getArea(self) -> float:
        return pi * (self.radius ** 2)

    def getPerimeter(self) -> float:
        return 2 * pi * self.radius

    def inside(self, point: Point2D) -> bool:
        # ponto está dentro se a distância ao centro for <= raio
        return hypot(point.x - self.center.x, point.y - self.center.y) <= self.radius

    def __str__(self) -> str:
        return f"{self.name}: C={self.center}, R={self.radius:.2f}"


# ===== Classe Rectangle =====
class Rectangle(Shape):
    def __init__(self, p1: Point2D, p2: Point2D):
        self.name = "Rect"
        self.p1 = p1  # vértice 1 (qualquer posição)
        self.p2 = p2  # vértice oposto

    def getName(self) -> str:
        return self.name

    def _dims(self):
        largura = abs(self.p1.x - self.p2.x)
        altura = abs(self.p1.y - self.p2.y)
        return largura, altura

    def getArea(self) -> float:
        largura, altura = self._dims()
        return largura * altura

    def getPerimeter(self) -> float:
        largura, altura = self._dims()
        return 2 * (largura + altura)

    def inside(self, point: Point2D) -> bool:
        min_x = min(self.p1.x, self.p2.x)
        max_x = max(self.p1.x, self.p2.x)
        min_y = min(self.p1.y, self.p2.y)
        max_y = max(self.p1.y, self.p2.y)
        return (min_x <= point.x <= max_x) and (min_y <= point.y <= max_y)

    def __str__(self) -> str:
        return f"{self.name}: P1={self.p1} P2={self.p2}"


# ===== Funções auxiliares =====
def show_shapes(shapes: list[Shape]) -> None:
    if not shapes:
        print("Shapes: []")
        return
    for i, s in enumerate(shapes):
        print(f"[{i}] {s} | área={s.getArea():.2f} | perímetro={s.getPerimeter():.2f}")


# ===== Função principal com comandos =====
if __name__ == "__main__":
    shapes: list[Shape] = []
    print("Comandos: ")
    print("  circle x y r        -> adiciona círculo (centro x,y; raio r)")
    print("  rect x1 y1 x2 y2    -> adiciona retângulo (vértices p1 e p2)")
    print("  inside i x y        -> verifica se ponto (x,y) está dentro da forma i")
    print("  show                -> mostra todas as formas com área e perímetro")
    print("  end                 -> encerra")
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
            if cmd == "circle" and len(parts) == 4:
                x, y, r = map(float, parts[1:])
                shapes.append(Circle(Point2D(x, y), r))

            elif cmd == "rect" and len(parts) == 5:
                x1, y1, x2, y2 = map(float, parts[1:])
                shapes.append(Rectangle(Point2D(x1, y1), Point2D(x2, y2)))

            elif cmd == "inside" and len(parts) == 4:
                i = int(parts[1])
                x, y = map(float, parts[2:])
                if i < 0 or i >= len(shapes):
                    print("fail: shape inexistente")
                else:
                    pt = Point2D(x, y)
                    res = shapes[i].inside(pt)
                    print("true" if res else "false")

            elif cmd == "show" and len(parts) == 1:
                show_shapes(shapes)

            elif cmd == "end" and len(parts) == 1:
                break

            else:
                print("fail: comando inválido")

        except Exception as e:
            print(f"fail: {e}")
