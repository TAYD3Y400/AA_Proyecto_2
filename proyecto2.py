import pygame, math

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

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


            
        

def input(event):
    if event.type == pygame.QUIT:
        exit(0)

x=300
y=550
angle=-90
depth=9
fork_angle=20
branch_angle=45
base_len=8
branch_base_len=5
branch_base=4

drawTree(x, y, angle, depth, fork_angle, branch_angle, base_len, branch_base_len, branch_base)


pygame.display.flip()
while True:
    input(pygame.event.wait())