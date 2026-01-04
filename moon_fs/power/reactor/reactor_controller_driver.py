import pygame

pygame.init()

display_size = (1920, 1080)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Janela de Exemplo")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))  # janela preta
    pygame.display.flip()

pygame.quit()
