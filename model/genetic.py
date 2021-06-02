from model.tree import Tree
from model.fractal import drawTree
import numpy as np
import random

# D: Funcion de fitness
# E: Dados unos resultados [AreaCubierta, AreaFuera] y unos pesos [w0, w1]
#    Obtiene el valor del fitness 
# R: len(weights) == len(results)
def fitness(results, weights, sums):
    fit = 0.0

    for i in range(len(results)):
        fit += results[i] * weights[i] + sums[i]
    
    fit = fit / len(results)

    return fit

# D: Genera una poblacion de parametros de arboles
# E: n es el tamano de la poblacion
def generate_pob(n, x = 300, y = 600):
    pob = []

    for i in range(n):
        tree = Tree()

        # La posicion en pantalla
        # Esto no influye en la forma del arbol
        tree.x1 = x
        tree.y1 = y
        
        # La base del tronco siempre es hacia arriba...
        tree.angle = -90

        # Se genera un angulo
        tree.fork_angle = random.randint(-45, 0)
        tree.branch_angle = random.randint(-60, 0)

        # Se genera la profundidad del arbol (10 es pesado)
        tree.depth = random.randint(1, 10)
        # Se genera el largo del tronco
        tree.base_len = random.randint(4, 10)
        tree.branch_base = random.randint(3, 10)
        # Se genera el numero de ramas
        tree.branches = random.randint(3, 5)

        pob.append(tree)

    return pob

# D: Retorna el valor Fitness de una poblacion
def sort_key(e):
    return e[0]

# D: Ordena las poblaciones en base a su fitness
# E: Un array de forma: [[Fitness, Arbol]]
def sort_pob(pob):
    return sorted(pob, key = sort_key, reverse=True)

# D: Dada una poblacion, las pone a prueba y determina el fitness de cada uno
def test_pob(population, areas, img, origin):
    weights = [100 / areas[0], -100 * 2 / areas[1], -1/100]
    sums = [0, 0, 1]
    res = []

    for i in range(len(population)):
        matrix = np.zeros((200, 200), dtype=int)

        print("Testeando individuo #", i)
        results = drawTree(population[i], None, img, origin, matrix)

        results[2] -= origin[1]
        results[2] = abs(200 - results[2])

        fit = fitness(results, weights, sums)

        res.append([fit, population[i]])

    print("Sorting")
    rst = sort_pob(res)

    return rst