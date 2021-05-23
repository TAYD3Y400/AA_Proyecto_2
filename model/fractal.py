def drawTree(x1, y1, angle, depth, fork_angle, branch_angle, base_len, branch_base, branches):
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle))*depth*base_len)
        y2 = y1 + int(math.sin(math.radians(angle))*depth*base_len)

        pygame.draw.line(screen, (255,255,255), (x1, y1), (x2, y2),2)


        for i in range(1,branches+1):

            if i<branches/2:
                drawTree(x2, y2, angle - fork_angle, depth - 1,branch_angle,branch_angle,branch_base, branch_base, branches)
            elif i>branches/2:
                drawTree(x2, y2, angle + fork_angle, depth - 1,branch_angle,branch_angle,branch_base, branch_base, branches)
            else:
                drawTree(x2, y2, angle, depth - 1,branch_angle,branch_angle,branch_base, branch_base, branches)
