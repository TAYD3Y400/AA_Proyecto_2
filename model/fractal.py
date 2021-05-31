import math
import pygame
import numpy as np
from model.tree import Tree

def sort_points(point_a, point_b):
    Points = [point_a, point_b]

    if point_a > point_b:
        Points = [point_b, point_a]

    return Points

def cast(point, min, max):
    if point < min:
        return min 
    
    if point > max:
        return max
        
    return point

def calc_area(point_a, point_b, img, origin):
    #dist_x = math.pow(point_a[0] - point_b[0], 2)
    #dist_y = math.pow(point_a[1] - point_b[1], 2)

    #dist = math.sqrt(dist_x + dist_y)

    #Xs = sort_points(point_a[0], point_b[0])
    #Ys = sort_points(point_a[1], point_b[1])

    #point_mid_x = int(Xs[0] + (Xs[1] - Xs[0])/2) - origin[0]
    #point_mid_y = int(Ys[0] + (Ys[1] - Ys[0])/2) - origin[1]
    #point_mid = [point_mid_x, point_mid_y]

    #if point_mid[0] < 0:
        #point_mid[0] = 0

    #if point_mid[1] < 0:
        #point_mid[1] = 0

    #result = [0, 0]
    #result[np.sum(img[point_mid[1]][point_mid[0]]) == 4] = int(dist)

    point_a = [point_a[0] - origin[0], point_a[1] - origin[1]]
    point_b = [point_b[0] - origin[0], point_b[1] - origin[1]]

    point_a = [cast(point_a[0], 0, 199), cast(point_a[1], 0, 199)]
    point_b = [cast(point_b[0], 0, 199), cast(point_b[1], 0, 199)]

    result = [0, 0]

    result[np.sum(img[point_a[1], point_a[0]]) == 4] += 1
    result[np.sum(img[point_b[1], point_b[0]]) == 4] += 1

    return result

def drawTree(tree_data, screen, img, origin):
    if tree_data.depth == 0:
        return [0, 0]

    areas = [0, 0]

    x2 = tree_data.x1 + int(math.cos(math.radians(tree_data.angle))*tree_data.depth*tree_data.base_len)
    y2 = tree_data.y1 + int(math.sin(math.radians(tree_data.angle))*tree_data.depth*tree_data.base_len)

    pygame.draw.line(screen, (255,0,0), (tree_data.x1, tree_data.y1), (x2, y2),2)

    area_covered = calc_area([tree_data.x1, tree_data.y1], [x2, y2], img, origin)

    areas[0] += area_covered[0]
    areas[1] += area_covered[1]

    for i in range(1,tree_data.branches+1):
        new_tree = Tree()
        new_tree.x1 = x2
        new_tree.y1 = y2
        new_tree.depth = tree_data.depth - 1
        new_tree.fork_angle = tree_data.branch_angle
        new_tree.branch_angle = tree_data.branch_angle
        new_tree.base_len = tree_data.branch_base
        new_tree.branch_base = tree_data.branch_base
        new_tree.branches = tree_data.branches

        if i<tree_data.branches/2:
            new_tree.angle = tree_data.angle - tree_data.fork_angle
            rst_areas = drawTree(new_tree, screen, img, origin)
        elif i>tree_data.branches/2:
            new_tree.angle = tree_data.angle + tree_data.fork_angle
            rst_areas = drawTree(new_tree, screen, img, origin)
        else:
            new_tree.angle = tree_data.angle
            rst_areas = drawTree(new_tree, screen, img, origin)

        areas[0] += rst_areas[0]
        areas[1] += rst_areas[1]
    
    return areas