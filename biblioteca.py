import pygame
import json
import time
from datos import lista

pygame.init()

# Constantes
ANCHO, ALTO = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (158, 209, 37)
YELLOW = (232, 214, 1)
BLUE = (0, 0, 255)
VIOLET = (221, 82, 193)
ORANGE = (235, 100, 33)
CYAN = (1, 127, 232)
FONT_SIZE = 24
BOTON_ANCHO, BOTON_ALTO = 200, 50
OPCION_ANCHO, OPCION_ALTO = 300, 50
CASILLA_ANCHO, CASILLA_ALTO = 70, 70
CASILLA_ESPACIADO = 20

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Carrera UTN")
icono = pygame.image.load("recursos\icon.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("recursos\escenario.png")
fondo_final = pygame.transform.scale(fondo, (ANCHO, ALTO))
font = pygame.font.Font(None, FONT_SIZE)
imagen_alumno = pygame.image.load("recursos\estudiante.png")
imagen_alumno = pygame.transform.scale(imagen_alumno,(70,140))

# Variables del juego
puntaje = 0
posicion = 0
pregunta_actual = 0
nombre = ""
preguntas = lista
clock = pygame.time.Clock()
start_time = 0
juego_iniciado = False

# Coordenadas de botones
button_start = pygame.Rect((ANCHO // 2 - BOTON_ANCHO // 2, ALTO // 2 - BOTON_ALTO // 2), (BOTON_ANCHO, BOTON_ALTO))
button_end = pygame.Rect((ANCHO // 2 - BOTON_ANCHO // 2, ALTO - 100), (BOTON_ANCHO, BOTON_ALTO))

opcion_a = pygame.Rect(300, 60, OPCION_ANCHO, OPCION_ALTO)
opcion_b = pygame.Rect(300, 130, OPCION_ANCHO, OPCION_ALTO)
opcion_c = pygame.Rect(300, 200, OPCION_ANCHO, OPCION_ALTO)


casillas = [pygame.Rect(0, 0, 0, 0),
            pygame.Rect(370, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(460, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(550, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(640, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(730, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(820, 370, CASILLA_ANCHO, CASILLA_ALTO), # Casilla "Avanza 1"
            pygame.Rect(910, 370, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(1000, 370, CASILLA_ANCHO, CASILLA_ALTO),

            pygame.Rect(1000, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(910, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(820, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(730, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(640, 460, CASILLA_ANCHO, CASILLA_ALTO),# Casilla "Retrocede 1"
            pygame.Rect(550, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(460, 460, CASILLA_ANCHO, CASILLA_ALTO),
            pygame.Rect(370, 460, CASILLA_ANCHO, CASILLA_ALTO),
            ]

personaje = pygame.Rect(280, 310,70, CASILLA_ALTO * 2)

def draw_txt(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    pantalla.blit(text_surface, (x, y))

def mostrar_menu_inicio():
    pantalla.fill(CYAN)
    draw_txt("Bienvenido a Carrera UTN", ANCHO // 2 - 100, ALTO // 2 - 100)
    pygame.draw.rect(pantalla, GREEN, button_start)
    draw_txt("Comenzar", button_start.x + 50, button_start.y + 15)
    pygame.display.flip()

def iniciar_juego():
    global juego_iniciado, pregunta_actual, puntaje, posicion
    pregunta_actual = 0
    puntaje = 0
    posicion = 0
    personaje.x = casillas[1].x - CASILLA_ANCHO - CASILLA_ESPACIADO
    personaje.y = casillas[1].y - 60
    juego_iniciado = True
    mostrar_pregunta()

def mostrar_pregunta():
    global start_time, pregunta_actual
    if pregunta_actual < len(preguntas):
        pregunta = preguntas[pregunta_actual]
        pantalla.fill(CYAN)
        pantalla.blit(fondo, (0, 0))
        draw_txt(f"Pregunta: {pregunta['pregunta']}", 300, 15)

        pygame.draw.rect(pantalla, YELLOW, opcion_a)
        draw_txt(f"a) {pregunta['a']}", opcion_a.x + 10, opcion_a.y + 10)

        pygame.draw.rect(pantalla, YELLOW, opcion_b)
        draw_txt(f"b) {pregunta['b']}", opcion_b.x + 10, opcion_b.y + 10)

        pygame.draw.rect(pantalla, YELLOW, opcion_c)
        draw_txt(f"c) {pregunta['c']}", opcion_c.x + 10, opcion_c.y + 10)

        if juego_iniciado:
            pygame.draw.rect(pantalla, RED, button_end)
            draw_txt("Terminar Juego", button_end.x + 20, button_end.y + 15)

        dibujar_pista()
        pygame.display.flip()
        start_time = time.time()
        temporizador(5, pregunta)
    else:
        finalizar_juego()

def dibujar_pista():
    for i, casilla in enumerate(casillas):
        if i % 2 == 0:
            pygame.draw.rect(pantalla, VIOLET, casilla)
        else:
            pygame.draw.rect(pantalla, ORANGE, casilla)
    draw_txt("Avanza 1",820,400)
    draw_txt("Retrocede 1",640,480)
    pygame.draw.rect(pantalla, WHITE, personaje)
    pantalla.blit(imagen_alumno,personaje)
    pygame.display.flip()

def temporizador(segundos, pregunta):
    global start_time
    running = True
    while running:
        tiempo_transcurrido = time.time() - start_time
        tiempo_restante = segundos - int(tiempo_transcurrido)
        if tiempo_restante <= 0:
            tiempo_restante = 0
            evaluar_respuesta('tiempo_agotado', pregunta)
            return

        pantalla.fill(CYAN, (1000, 10, 240, 50))
        draw_txt(f"Tiempo restante: {tiempo_restante} segundos", 1000, 10)
        draw_txt(f"Puntuación: {puntaje}", 1000, 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if opcion_a.collidepoint(event.pos):
                    evaluar_respuesta('a', pregunta)
                    running = False
                elif opcion_b.collidepoint(event.pos):
                    evaluar_respuesta('b', pregunta)
                    running = False
                elif opcion_c.collidepoint(event.pos):
                    evaluar_respuesta('c', pregunta)
                    running = False
                elif button_end.collidepoint(event.pos):
                    finalizar_juego()
                    return

        clock.tick(30)

def evaluar_respuesta(respuesta, pregunta):
    global puntaje, posicion, pregunta_actual, personaje

    if respuesta == pregunta['correcta']:
        print("¡Correcto!")
        puntaje += 10
        posicion += 2
    else:
        print("Incorrecto.")
        if posicion > 0:
            posicion -= 1

    personaje.x = casillas[min(posicion, len(casillas) - 1)].x
    personaje.y = casillas[min(posicion, len(casillas) - 1)].y - 60

    if respuesta == pregunta['correcta']:
        if personaje.colliderect(casillas[6]):  # Casilla "Avanza 1"
            posicion += 1
            personaje.x = casillas[min(posicion, len(casillas) - 1)].x
            personaje.y = casillas[min(posicion, len(casillas) - 1)].y - 60
        elif personaje.colliderect(casillas[13]):  # Casilla "Retrocede 1"
            posicion -= 2
            personaje.x = casillas[min(posicion, len(casillas) - 1)].x
            personaje.y = casillas[min(posicion, len(casillas) - 1)].y - 60

    if posicion >= 17:
        finalizar_juego()
    elif posicion == 0:
        pregunta_actual += 1
        personaje.x = casillas[1].x - CASILLA_ANCHO - CASILLA_ESPACIADO
        personaje.y = casillas[1].y - 60
        mostrar_pregunta()
    else:
        pregunta_actual += 1
        mostrar_pregunta()


def finalizar_juego():
    global juego_iniciado
    juego_iniciado = False
    print(f"Fin del juego. Tu puntaje final es: {puntaje}")
    pedir_nombre()

def pedir_nombre():
    nombre = ""
    input_active = True
    while input_active:
        pantalla.fill(CYAN)
        draw_txt("Ingresa tu nombre:", 50, 50)
        draw_txt(nombre, 50, 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    guardar_puntaje(nombre)
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode


def guardar_puntaje(nombre):
    try:
        with open("puntajes.json", "r") as file:
            puntajes = json.load(file)
    except FileNotFoundError:
        puntajes = []

    puntajes.append({"nombre": nombre, "puntaje": puntaje})
    puntajes = sorted(puntajes, key=lambda x: x['puntaje'], reverse=True)[:10]

    with open("puntajes.json", "w") as file:
        json.dump(puntajes, file, indent=4)

    mostrar_top_puntajes(puntajes)

def mostrar_top_puntajes(puntajes):
    pantalla.fill(CYAN)
    draw_txt("Top 10 puntajes:", 50, 50)
    y_puntaje = 100
    for i, p in enumerate(puntajes):
        draw_txt(f"{i+1}. {p['nombre']}: {p['puntaje']} puntos", 50, y_puntaje)
        y_puntaje += 30

    pygame.display.flip()
    pygame.time.wait(5000)
    mostrar_menu_inicio()
