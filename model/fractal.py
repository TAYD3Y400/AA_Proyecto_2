import math
import pygame
import numpy as np
import random
from model.tree import Tree

def renderTree(screen, tree, x2, y2):
    rgb = (random.randint(100, 200), random.randint(50, 100), random.randint(200, 255))

    if tree.depth == 1:
        rgb = (random.randint(200, 255), random.randint(0, 20), random.randint(0, 50))

    pygame.draw.line(screen, rgb, (tree.x1, tree.y1), (x2, y2), 2)

    pygame.display.update()

# D: Evita que un punto sobrepase el min y max
#    Por default los bordes son oscuros asi que esto es una penalizacion
# E: Un valor x, y un minimo para ese x y un max para ese x
def cast(point, min, max):
    if point < min or point > max:
        return max 
        
    return point

# D: Determina si el punto a esta dentro del area
# E: Un punto [x, y], una matriz que represente una imagen RGB normalizada, un punto origen del punto, y una matriz
def calc_area(point_a, img, origin, matrix):
    point_a = [point_a[0] - origin[0], point_a[1] - origin[1]]

    point_a = [cast(point_a[0], 0, 199), cast(point_a[1], 0, 199)]

    result = [0, 0]

    if matrix[point_a[0]][point_a[1]] == 0:
        isWhite = np.sum(img[point_a[1], point_a[0]]) == 4
        
        matrix[point_a[0]][point_a[1]] = 1
        result[isWhite] += 1

    return result

def getArea(areas, tree_data, img, origin, matrix, x2, y2):
    area_covered = calc_area([tree_data.x1, tree_data.y1], img, origin, matrix)

    areas[0] += area_covered[0]
    areas[1] += area_covered[1]

    area_covered = calc_area([x2, y2], img, origin, matrix)

    areas[0] += area_covered[0]
    areas[1] += area_covered[1]

    return areas

# D: Funcion fractal para el arbol, si shouldRender es True dibuja sobre la screen
# E: Un Tree con los parametros del arbol, un screen de Python, un punto origen, una matriz por referencia
def drawTree(tree_data, screen, img, origin, matrix, shouldRender = False):
    if tree_data.depth == 0:
        return [0, 0, 200, 0]

    x2 = tree_data.x1 + int(math.cos(math.radians(tree_data.angle))*tree_data.depth*tree_data.base_len)
    y2 = tree_data.y1 + int(math.sin(math.radians(tree_data.angle))*tree_data.depth*tree_data.base_len)

    areas = [0, 0, cast(tree_data.y1, 0, 199), 0]

    if y2 < tree_data.y1:
        areas[2] = cast(y2, 0, 199)

    if shouldRender:
        renderTree(screen, tree_data, x2, y2)
    else:
        areas = getArea(areas, tree_data, img, origin, matrix, x2, y2)

    k = 0

    for i in range(0, tree_data.branches):
        new_tree = Tree()
        new_tree.x1 = x2
        new_tree.y1 = y2
        new_tree.depth = tree_data.depth - 1
        new_tree.fork_angle = tree_data.branch_angle + random.randint(-2, 2)
        new_tree.branch_angle = tree_data.branch_angle
        new_tree.base_len = tree_data.branch_base
        new_tree.branch_base = tree_data.branch_base
        new_tree.branches = tree_data.branches

        sign = 1

        if i % 2 == 0:
            sign = -1

        new_tree.angle = tree_data.angle + sign * tree_data.fork_angle * k
        
        rst_areas = drawTree(new_tree, screen, img, origin, matrix, shouldRender)

        areas[0] += rst_areas[0]
        areas[1] += rst_areas[1]

        if rst_areas[2] < areas[2]:
            areas[2] = rst_areas[2]

        if i % 2 == 0:
            k += 1

    return areas