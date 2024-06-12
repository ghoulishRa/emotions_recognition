import pygame
import time

# Inicializar pygame
pygame.init()

# Configurar el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar y redimensionar la imagen
image = pygame.image.load("sorpresa.jpg")
image = pygame.transform.scale(image, (200, 200))
image_rect = image.get_rect()
image_rect.topleft = (screen_width - image_rect.width, 0)  # Ubicar la imagen en la esquina superior derecha

# Configurar el título de la ventana
pygame.display.set_caption("Pantalla Intermitente de Colores con Imagen")

# Definir los colores
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Función para mostrar la pantalla de colores intermitentes
def flash_screen(duration, interval, color):
    start_time = time.time()
    while time.time() - start_time < duration:
        screen.fill(color)
        screen.blit(image, image_rect)  # Dibujar la imagen encima del color
        pygame.display.update()
        time.sleep(interval)
        screen.fill(BLACK)
        screen.blit(image, image_rect)  # Dibujar la imagen encima del color
        pygame.display.update()
        time.sleep(interval)

def flash_color_screen(duration, interval):
    start_time = time.time()
    colors = [BLUE, GREEN, RED]
    color_index = 0
    while time.time() - start_time < duration:
        screen.fill(colors[color_index])  # Llenar todo el área de color
        screen.blit(image, image_rect)  # Dibujar la imagen encima del color
        pygame.display.update()
        time.sleep(interval)
        screen.fill(BLACK)  # Llenar todo el área de negro
        screen.blit(image, image_rect)  # Dibujar la imagen encima del color
        pygame.display.update()
        time.sleep(interval)
        color_index = (color_index + 1) % len(colors)

# Funciones PCA
def pca_alto():
    flash_screen(3, 0.1, BLUE)
    flash_screen(6, 0.5, GREEN)
    flash_color_screen(9, 0.9)

def pca_medio():
    flash_screen(3, 0.9, BLUE)
    flash_color_screen(15, 0.9)

def pca_bajo():
    flash_screen(3, 0.1, RED)
    flash_screen(6, 0.5, GREEN)
    flash_screen(9, 0.1, BLUE)

# Funciones PRC
def prc_alto():
    flash_screen(3, 0.1, BLUE)
    flash_screen(6, 0.5, RED)
    flash_color_screen(9, 0.9)

def prc_medio():
    flash_screen(3, 0.9, BLUE)
    flash_color_screen(6, 0.9)
    flash_screen(9, 0.9, BLUE)

def prc_bajo():
    flash_screen(3, 0.1, RED)
    flash_screen(6, 0.5, GREEN)
    flash_screen(9, 0.9, BLUE)

# Funciones PRM
def prm_alto():
    flash_screen(3, 0.1, RED)
    flash_screen(6, 0.5, RED)
    flash_color_screen(9, 0.9)

def prm_medio():
    flash_screen(3, 0.9, BLUE)
    flash_color_screen(6, 0.9)
    flash_screen(9, 0.9, BLUE)

def prm_bajo():
    flash_screen(3, 0.1, RED)
    flash_screen(6, 0.5, GREEN)
    flash_screen(9, 0.9, BLUE)

# Ejecutar la función de intermitencia por 5 segundos con un intervalo de 0.9 segundos
prc_alto()

# Cerrar pygame
pygame.quit()
