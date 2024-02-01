import pygame

DEBUG_INFO = None
FONT_SIZE = 30
INFO_X = 10
INFO_Y = 10

pygame.init()
font = pygame.font.Font(None, FONT_SIZE)

def debug(info):
    global DEBUG_INFO
    DEBUG_INFO = info

def debug_draw():
    global DEBUG_INFO

    if DEBUG_INFO is not None:
        if isinstance(DEBUG_INFO, str):
            DEBUG_INFO = [DEBUG_INFO]
        if not isinstance(DEBUG_INFO, list):
            DEBUG_INFO = ["<invalid>"]
        else:
            display_surf = pygame.display.get_surface()
            y = INFO_Y
            for message in DEBUG_INFO:
                if not isinstance(message, str):
                    message = "<invalid>"
                debug_surf = font.render(message, True, 'white')
                debug_rect = debug_surf.get_rect(topleft=(INFO_X, y))
                pygame.draw.rect(display_surf, 'black', debug_rect)
                display_surf.blit(debug_surf, debug_rect)
                y += FONT_SIZE

        DEBUG_INFO = None
