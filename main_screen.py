import sys
import pygame

# Set up the Pygame window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Main Screen")
alpha = 255
fade_rate = 5
screen.set_alpha(alpha)

ms_active = True
maingame = False

while ms_active:
    # Set up the title text
    title_font = pygame.font.Font(None, 96)
    title_text = title_font.render("COMETS", True, (0, 0, 0))
    title_rect = title_text.get_rect()
    title_rect.center = (400, 150)

    # Set up the creator's name text
    creator_font = pygame.font.Font(None, 48)
    creator_text = creator_font.render("by Daniela Castro and Vitória Rodrigues", True, (0, 0, 0))
    creator_rect = creator_text.get_rect()
    creator_rect.center = (400, 200)

    # Set up the menu options
    menu_font = pygame.font.Font(None, 72)
    start_text = menu_font.render("START", True, (0, 0, 0))
    start_rect = start_text.get_rect()
    start_rect.center = (400, 300)
    quit_text = menu_font.render("QUIT", True, (0, 0, 0))
    quit_rect = quit_text.get_rect()
    quit_rect.center = (400, 400)

    # Set up the selected option
    selected_option = 0

    # Clear the screen
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ms_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = max(0, selected_option - 1)
            elif event.key == pygame.K_DOWN:
                selected_option = min(1, selected_option + 1)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    ms_active = False
                    maingame = True
                else:
                    sys.exit()

    # Draw the title and creator's name
    screen.blit(title_text, title_rect)
    screen.blit(creator_text, creator_rect)

    # Draw the menu options
    if selected_option == 0:
        screen.blit(menu_font.render("START", True, (255, 0, 0)), start_rect)
        screen.blit(quit_text, quit_rect)
    else:
        screen.blit(start_text, start_rect)
        screen.blit(menu_font.render("QUIT", True, (255, 0, 0)), quit_rect)

    # Update the display
    pygame.display.flip()


if not ms_active:
    while alpha > 0:
        # Decrease the alpha value
        alpha -= fade_rate

        # Clamp the alpha value to the range 0-255
        alpha = max(alpha, 0)

        # Set the alpha value of the screen surface
        screen.set_alpha(alpha)

        # Update the display
        pygame.display.flip()
    maingame = True
    pass
