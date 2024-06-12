import cv2
import pygame
from mask_functions import setup_camera, get_kernel, get_color_ranges, detect_color, show_images
import protocol_functions as pf

def main():
    cap = setup_camera()
    kernel = get_kernel()
    color_ranges = get_color_ranges()
    
    save = 0
    num_class = 0
    protocol_flag = False
    
    while True:
        result, frame, closing = detect_color(cap, kernel, color_ranges)
        
        print(save)
        
        if save == 100:
            protocol_flag = True
            num_class = result
            break
        else:
            protocol_flag = False
            save += 1
        
        if result is not None: 
            print(f'Detected Result: {result}')
        
        if frame is not None and closing is not None:
            show_images(frame, closing)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
    if protocol_flag:
        altura = int(input("ingresa altura: "))  # Convertir altura a entero
        print(altura)
        print(num_class)
        
        # Inicializar Pygame
        pygame.init()

        # Configuración de la pantalla
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Parpadeo de Pantalla")

        # Seleccionar la función a ejecutar
        if num_class == 1:
            if altura == 1:
                current_function = pf.pca_alto
            elif altura == 2:
                current_function = pf.pca_medio
            elif altura == 3:
                current_function = pf.pca_bajo
            else:
                current_function = pf.paint_black_screen
                

        elif num_class == 2:
            if altura == 1:
                current_function = pf.prm_alto
            elif altura == 2:
                current_function = pf.prm_medio
            elif altura == 3:
                current_function = pf.prm_bajo
            else:
                current_function = pf.paint_black_screen
                
        elif num_class == 3:
            if altura == 1:
                current_function = pf.prc_alto
                print("prc alto")
            elif altura == 2:
                current_function = pf.prc_medio
                print("prc alto")
            elif altura == 3:
                current_function = pf.prc_bajo
                print("prc alto")
            else:
                current_function = pf.paint_black_screen
                print("else")
        else:
            print("Input no válido")
            pygame.quit()
            exit()

        # Ejemplo de uso
        running = True
        start_time = pygame.time.get_ticks()
        stage = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(pf.BLACK)
            stage, start_time = current_function(screen, stage, start_time)

            pygame.display.flip()
            
            if stage > 2:
                running = False  # Termina el programa una vez que todas las etapas se han completado

        pygame.quit()
        

if __name__ == "__main__":
    main()

