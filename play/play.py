import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

pygame.display.get_surface().fill((100, 100, 100))
pygame.display.flip()

running = True
while running:
    print(pygame.event.get())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()