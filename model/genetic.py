from model.tree import Tree
from model.fractal import drawTree
import numpy as np
import random
import time

# D: Funcion de fitness
# E: Dados unos resultados [AreaCubierta, AreaFuera] y unos pesos [w0, w1]
#    Obtiene el valor del fitness 
# R: len(weights) == len(results)
def fitness(results, weights, sums):
    fit = 0.0

    for i in range(len(results)):
        fit += results[i] * weights[i] + sums[i]

    return fit

# D: Genera una poblacion de parametros de arboles
# E: n es el tamano de la poblacion
def generate_pob(n, x, y):
    pob = []

    for i in range(n):
        random.seed(time.clock())
        tree = Tree()

        # La posicion en pantalla
        # Esto no influye en la forma del arbol
        tree.x1 = x
        tree.y1 = y
        
        # La base del tronco siempre es hacia arriba...
        tree.angle = -90

        # Se genera un angulo
        tree.fork_angle = random.randint(-63, 0)
        tree.branch_angle = random.randint(-63, 0)

        # Se genera la profundidad del arbol (10 es pesado)
        tree.depth = random.randint(1, 8)
        # Se genera el largo del tronco
        tree.base_len = random.randint(4, 7)
        tree.branch_base = random.randint(3, 7)
        # Se genera el numero de ramas
        tree.branches = 3

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
    # [Area negra, area blanca, distancia de la altura, Monte Carlo]
    weights = [2/ areas[0], -5 / areas[1], -0.5/200, 5/1000]
    sums = [0, 5, 0.5, 0]
    res = []

    for i in range(len(population)):
        matrix = np.zeros((200, 200), dtype=int)
        
        results = [0, 0, 200, 0]

        results = drawTree(population[i], None, img, origin, matrix)

        # Montecarlo
        sum = 0
        for k in range(1000):
            random.seed(time.clock())
            x = random.randint(0, len(img) - 1)
            y = random.randint(0, len(img) - 1)

            if np.sum(img[y][x]) == 4 and matrix[x][y] == 1:
                sum += 1

        results[3] = sum

        fit = fitness(results, weights, sums)

        res.append([fit, population[i]])

    rst = sort_pob(res)

    return rst

# Given two numbers, merge its bits in some range
def merge_nums(num1, num2):
    random.seed(time.clock())
    values = [2, 3]
    binary = ["1", "0"]

    a = (bin(num1))[values[num1 < 0]:]
    b = (bin(num2))[values[num2 < 0]:]

    nums = [a, b]

    if len(b) > len(a):
        nums = [b, a]

    dif = abs(len(a) - len(b))

    nums[1] = '0'*dif + nums[1]

    min_ = random.randint(0, len(nums[0]))
    max_ = random.randint(min_, len(nums[0]))

    selected = random.randint(0, 1)

    generated = nums[selected][0:min_]
    generated += nums[abs(selected-1)][min_:max_]
    generated += nums[selected][max_:]

    # Mutacion
    temp = generated
    i = random.randint(0, len(temp)-1)
    generated = temp[:i]
    generated += binary[temp[i] == "1"]
    generated += temp[i+1:]

    if num1 < 0 and num2 < 0:
        generated = '-' + generated

    return int(generated, 2)

# Given two trees, it generates a tree merge of these ones
def merge_tree(tree_a, tree_b):
    random.seed(time.clock())
    gen_tree = Tree()
    trees = [tree_a, tree_b]

    gen_tree.fathers = trees

    # Estos valores son constantes
    gen_tree.x1 = tree_a.x1
    gen_tree.y1 = tree_a.y1
    gen_tree.angle = tree_a.angle

    # Estos valores mutan
    gen_tree.branches = merge_nums(trees[0].branches, trees[1].branches)
    gen_tree.base_len = merge_nums(trees[0].base_len, trees[1].base_len)
    gen_tree.depth = merge_nums(trees[0].depth - 1, trees[1].depth - 1) + 1

    gen_tree.fork_angle = merge_nums(trees[0].fork_angle, trees[1].fork_angle) + random.randint(-3, 3)

    gen_tree.branch_angle = merge_nums(trees[0].branch_angle, trees[1].branch_angle) + random.randint(-3, 3)
    gen_tree.branch_base_len = merge_nums(trees[0].branch_base_len, trees[1].branch_base_len)
    gen_tree.branch_base = merge_nums(trees[0].branch_base, trees[1].branch_base)

    return gen_tree

# Given a population, gets the the top 50% and 
# generates a new generation and append it
# Also agregates a new random tree
def merge(population, origin):
    gen_size = int(len(population)*0.4)
    top = population[:gen_size]

    new_gen = generate_pob(int(len(population)*0.1), origin[0] + 100, origin[1] + 200)

    new_gen.extend(top)

    for i in range(int(len(population)*0.6)):
        tree_a = top[random.randint(0, len(top) - 1)]
        tree_b = top[random.randint(0, len(top) - 1)]

        new_tree = merge_tree(tree_a, tree_b)

        new_gen.append(new_tree)

    return new_gen