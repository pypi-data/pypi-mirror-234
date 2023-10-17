from math import factorial, cos, sin, radians

def bezier_equiv_coord(c: float, c0: float, c2: float):
   return 2 * c - 0.5 * (c0 + c2)

def bernstein_polynomial(index: int, grade: int, region: float):
   # Renomeando Parâmetros para Facilitar os Cálculos
   i, p, t = index, grade, region
   
   # Verificando Validade dos Parâmetros
   if i < 0 or i > p:
      raise ValueError(f'Index {i} does not exist for Bernstein Polynomial with Grade {p}.')
   
   # Calculando Polinômio na Região Informada
   return (factorial(p) / (factorial(i) * factorial(p - i))) * t ** i * (1 - t) ** (p - i)

def projection_isometric(x: float, y: float, z: float):
   theta = radians(30)
   u = x * cos(theta) - y * cos(theta)
   v = x * sin(theta) + y * sin(theta) + z
   return u, v