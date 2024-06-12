import pygame

# Definir los colores
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)

# Secuencia de colores
color_sequences = [RED, BLUE, GREEN]

# Función para manejar el parpadeo de pantalla
def flash_screen_logic(screen, start_time, duration, interval, color, color_name):
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time < duration:
        if int(elapsed_time / interval) % 2 == 0:
            screen.fill(color)
            draw_text(screen, color_name, (10, 10))
        else:
            screen.fill(BLACK)
        pygame.display.update()
        return False
    return True

# Función para manejar el parpadeo de colores
def flash_color_screen_logic(screen, start_time, duration, interval, colors, color_names):
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time < duration:
        current_color_index = int(elapsed_time / interval) % len(colors)
        current_color = colors[current_color_index]
        current_color_name = color_names[current_color_index]
        if int(elapsed_time / (interval / 2)) % 2 == 0:
            screen.fill(current_color)
            draw_text(screen, current_color_name, (10, 10))
        else:
            screen.fill(BLACK)
        pygame.display.update()
        return False
    return True

# Función para dibujar el texto
def draw_text(screen, text, position):
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

# Definir las etapas de PCA, PRC y PRM

##definiendo pca

def pca_alto(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, BLUE, "PCA: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, GREEN, "PCA: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_color_screen_logic(screen, start_time, 9, 0.9, color_sequences, ["PCA: Alto", "PCA: Alto", "PCA: Alto"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def pca_medio(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.9, BLUE, "PCA: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 0, 0.9, BLUE, "PCA: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_color_screen_logic(screen, start_time, 15, 0.9, color_sequences, ["PCA: Medio", "PCA: Medio", "PCA: Medio"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def pca_bajo(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, RED, "PCA: Bajo"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, GREEN, "PCA: Bajo"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_screen_logic(screen, start_time, 9, 0.1, BLUE, "PCA: Bajo"):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

## definiendo prc

def prc_alto(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, BLUE, "PRC: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, RED, "PRC: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_color_screen_logic(screen, start_time, 9, 0.9, color_sequences, ["PRC: Alto", "PRC: Alto", "PRC: Alto"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def prc_medio(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, BLUE, "PRC: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_color_screen_logic(screen, start_time, 6, 0.9, color_sequences, ["PRC: Medio", "PRC: Medio", "PRC: Medio"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_screen_logic(screen, start_time, 9, 0.9, BLUE, "PRC: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def prc_bajo(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, RED, "PRC: Bajo"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, RED, "PRC: Bajo"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_color_screen_logic(screen, start_time, 9, 0.9, color_sequences, ["PRC: Bajo", "PRC: Bajo", "PRC: Bajo"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

## defininendo prm

def prm_alto(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, RED, "PRM: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, RED, "PRM: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_color_screen_logic(screen, start_time, 9, 0.9, color_sequences, ["PRM: Alto", "PRM: Alto", "Alto"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def prm_medio(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.9, BLUE, "PRM: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_color_screen_logic(screen, start_time, 6, 0.9, color_sequences, ["PRM: Medio", "PRM: Medio", "Medio"]):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_screen_logic(screen, start_time, 9, 0.9, BLUE, "PRM: Medio"):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time

def prm_bajo(screen, stage, start_time):
    if stage == 0:
        if flash_screen_logic(screen, start_time, 3, 0.1, RED, "PRM: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 1:
        if flash_screen_logic(screen, start_time, 6, 0.5, GREEN, "PRM: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    elif stage == 2:
        if flash_screen_logic(screen, start_time, 9, 0.9, RED, "PRM: Alto"):
            stage += 1
            start_time = pygame.time.get_ticks()
    return stage, start_time
