import heapq
import pygame.freetype

# Estado global del highlight (controlado solo por a_star)
HIGHLIGHT_NODE = None

# Mapa de ids a nombre
NODOS_DICT = {
    1: "raiz_pos",
    2: "raiz_subarbol_izquierdo_pos",
    3: "raiz_subarbol_derecho_pos",
    4: "nodo1_subarbol_izquierdo_pos",
    5: "nodo2_subarbol_izquierdo_pos",
    6: "nodo1_subarbol_derecho_pos",
    7: "nodo2_subarbol_derecho_pos",
}

is_running = False
recorrido_path = []  # Almacena el recorrido generado
current_index = 0
last_update_time = 0
UPDATE_INTERVAL = 500  # Milisegundos entre actualizaciones

# Definición del árbol binario (estructura: nodo_id -> (hijo_izquierdo, hijo_derecho))
ARBOL = {
    1: (2, 3), # Nodo raiz
    2: (4, 5), # Nodo raiz subárbol izquierdo
    3: (6, 7), # Nodo raiz subárbol derecho
    4: (None, None), # Nodo izquierdo subárbol izquierdo
    5: (None, None), # Nodo derecho subárbol izquierdo
    6: (None, None), # Nodo izquierdo subárbol derecho
    7: (None, None), # Nodo derecho subárbol derecho
}

OBJETIVO = 7  # Nodo objetivo por defecto (Biblioteca)

# Heurística: distancia en niveles hasta el objetivo
NIVEL = {
    1: 0,
    2: 1, 3: 1,
    4: 2, 5: 2, 6: 2, 7: 2
}

def heuristica(nodo):
    return abs(NIVEL[nodo] - NIVEL[OBJETIVO])

def a_star_path(inicio, objetivo):
    frontera = []
    heapq.heappush(frontera, (0 + heuristica(inicio), 0, inicio, [inicio]))
    visitados = set()
    while frontera:
        f, g, actual, camino = heapq.heappop(frontera)
        if actual == objetivo:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        hijos = ARBOL.get(actual, (None, None))
        for hijo in hijos:
            if hijo is not None and hijo not in visitados:
                heapq.heappush(frontera, (g+1+heuristica(hijo), g+1, hijo, camino+[hijo]))
    return []

def iniciar_ejecucion(current_time):
    global is_running, current_index, last_update_time, recorrido_path
    current_index = 0
    last_update_time = current_time
    recorrido_path = a_star_path(1, OBJETIVO)
    is_running = True


def a_star(current_time):
    global HIGHLIGHT_NODE, current_index, last_update_time, recorrido_path, is_running
    if not is_running:
        HIGHLIGHT_NODE = None
        return
    if not recorrido_path:
        HIGHLIGHT_NODE = None
        return
    if current_time - last_update_time >= UPDATE_INTERVAL:
        if current_index < len(recorrido_path):
            node_id = recorrido_path[current_index]
            HIGHLIGHT_NODE = NODOS_DICT[node_id]
            current_index += 1
            last_update_time = current_time
        else:
            HIGHLIGHT_NODE = None
            is_running = False


if __name__ == "__main__":
    width = 1024
    height = 720
    move = 85
    pygame.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A*")
    ft_font = pygame.freetype.SysFont("DejaVu Sans", 28, bold=True)


    def draw_label(surface, letter, pos, color=(255, 255, 255)):
        text_surf, text_rect = ft_font.render(letter, color)
        text_rect.center = (int(pos[0]), int(pos[1]))
        surface.blit(text_surf, text_rect)


    # Definir botón en la parte inferior
    boton_y = height - 75
    run_rect = pygame.Rect(50, boton_y, 240, 50)

    running = True
    clock = pygame.time.Clock()
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if run_rect.collidepoint(mouse_pos):
                    iniciar_ejecucion(current_time)

        a_star(current_time)
        clock.tick(60)
        screen.fill((255, 255, 255))

        # Dibujar botón en la parte inferior
        pygame.draw.rect(screen, (100, 255, 100), run_rect)
        ft_font.render_to(screen, (run_rect.x + 50, run_rect.y + 15), "Ejecutar", (0, 0, 0))

        # Posiciones por nombre
        nodos_pos = {
            NODOS_DICT[1]: ((width / 2) - move, 75),
            NODOS_DICT[2]: (width - 660 - move, height / 4),
            NODOS_DICT[3]: (width - 360 - move, height / 4),
            NODOS_DICT[4]: (width - 740 - move, height / 2.2),
            NODOS_DICT[5]: (width - 580 - move, height / 2.2),
            NODOS_DICT[6]: (width - 425 - move, height / 2.2),
            NODOS_DICT[7]: (width - 245 - move, height / 2.2),
        }
        circle_radius = 40
        # Líneas conectoras
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[1]], nodos_pos[NODOS_DICT[2]], 2)
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[1]], nodos_pos[NODOS_DICT[3]], 2)
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[2]], nodos_pos[NODOS_DICT[4]], 2)
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[2]], nodos_pos[NODOS_DICT[5]], 2)
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[3]], nodos_pos[NODOS_DICT[6]], 2)
        pygame.draw.line(screen, (0, 0, 0), nodos_pos[NODOS_DICT[3]], nodos_pos[NODOS_DICT[7]], 2)
        # Ovalo raíz
        oval_rect = pygame.Rect(0, 0, 160, 60)
        oval_rect.center = (int(nodos_pos[NODOS_DICT[1]][0]), int(nodos_pos[NODOS_DICT[1]][1]))
        color_raiz = (255, 0, 0) if HIGHLIGHT_NODE == NODOS_DICT[1] else (120, 120, 120)
        pygame.draw.ellipse(screen, color_raiz, oval_rect)
        # Círculos intermedios
        for i in [2, 3, 4, 5, 6]:
            color_nodo = (255, 0, 0) if HIGHLIGHT_NODE == NODOS_DICT[i] else (120, 120, 120)
            pygame.draw.circle(screen, color_nodo, nodos_pos[NODOS_DICT[i]], circle_radius)
        # Ovalo objetivo
        oval_rect = pygame.Rect(0, 0, 180, 80)
        oval_rect.center = (
            int(nodos_pos[NODOS_DICT[7]][0]),
            int(nodos_pos[NODOS_DICT[7]][1]),
        )
        color_objetivo = (255, 0, 0) if HIGHLIGHT_NODE == NODOS_DICT[7] else (120, 120, 120)
        pygame.draw.ellipse(screen, color_objetivo, oval_rect)
        # Letras
        draw_label(screen, "Entrada", nodos_pos[NODOS_DICT[1]])
        draw_label(screen, "B", nodos_pos[NODOS_DICT[2]])
        draw_label(screen, "C", nodos_pos[NODOS_DICT[3]])
        draw_label(screen, "D", nodos_pos[NODOS_DICT[4]])
        draw_label(screen, "E", nodos_pos[NODOS_DICT[5]])
        draw_label(screen, "F", nodos_pos[NODOS_DICT[6]])
        draw_label(screen, "Biblioteca", nodos_pos[NODOS_DICT[7]])
        # Mostrar recorrido A*
        ft_font.render_to(screen, (50, 600), f"Recorrido A*: {recorrido_path}", (80, 80, 80))
        pygame.display.flip()
    pygame.quit()
