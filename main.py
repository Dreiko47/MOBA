import pygame
import csv
import constante_1
from Personaje import Personaje
import objetos_test
import trainMOBAgents_quasi
from weapon import Weapon
import os
from Textos import DamageText
import time
import AvatarAtacante

# Dimensiones del mapa
MAP_WIDTH = 5000
MAP_HEIGHT = 5000

# Variables del ataque especial
ataque_especial = False
tiempo_ultimo_ataque_especial = 0
TIEMPO_ENFIRAMIENTO = 90  # 1 minuto y 30 segundos
DURACION_ATAQUE_ESPECIAL = 10  # Duración del ataque especial en segundos

# Inicialización del avatar
avatar = AvatarAtacante.AvatarAtacante(x=constante_1.ANCHO_VENTANA // 2, y=constante_1.ALTO_VENTANA // 2)

# Inicializar objetos_frame
objetos_frame = {}

# Definir un mapa sencillo
tu_mapa = [
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0]
]

# Asignar el mapa al avatar
avatar.lecturaMapa(tu_mapa)

# Funciones:
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

def contar_elementos(directorio):
    return len(os.listdir(directorio))

def nombre_carpetas(directorio):
    return os.listdir(directorio)

pygame.init()

ventana = pygame.display.set_mode((constante_1.ANCHO_VENTANA, constante_1.ALTO_VENTANA))
pygame.display.set_caption("Proyecto CIC_MOBA")

font = pygame.font.Font("assets//Fonts//mago2.ttf", 80)

background_image = pygame.image.load('assets//images//Escenarios//Fondo_pasto.png')
bg_width, bg_height = background_image.get_size()

animaciones = []
for i in range(7):
    img = pygame.image.load(f"assets//images//characters/Player/player_{i}.png").convert_alpha()
    img = escalar_img(img, constante_1.SCALA_PERSONAJE)
    animaciones.append(img)

directorio_enemigos = "assets//images//characters//Enemigos"
tipo_enemigos = nombre_carpetas(directorio_enemigos)
animacion_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//Enemigos//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constante_1.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animacion_enemigos.append(lista_temp)

imagen_Baculo = pygame.image.load(f"assets//images//Weaponds//Magico 0.png").convert_alpha()
imagen_Baculo = escalar_img(imagen_Baculo, constante_1.SCALA_BACULO)

imagen_BLuz = pygame.image.load(f"assets//images//Weaponds//BLuz.png").convert_alpha()
imagen_BLuz = escalar_img(imagen_BLuz, constante_1.SACALA_BLUZ)

tile_list = []
for x in range(constante_1.TILE_TYPES):
    tile_image = pygame.image.load(f"assets//images//Tiles//tile_{x + 1}.png")
    tile_image = pygame.transform.scale(tile_image, (constante_1.TILE_SIZE, constante_1.TILE_SIZE))
    tile_list.append(tile_image)

# Cargar las imágenes de los árboles
arbol_image = pygame.image.load(f"assets//images//Plantas//Arbol_1.png").convert_alpha()
arbol_image = escalar_img(arbol_image, 0.6)

# Definir las posiciones de los árboles en el mapa
posiciones_arboles = [(500, 300), (1000, 800), (1500, 1200), (2000, 500), (2500, 1500)]

# Crear rectángulos de colisión para los árboles
rectangulos_arboles = [arbol_image.get_rect(topleft=pos) for pos in posiciones_arboles]

# Dibuja cuadricula en pantalla para mediciones
def dibujar_grid():
    for x in range(40):
        pygame.draw.line(ventana, constante_1.BLANCO, (x * constante_1.TILE_SIZE, 0), (x * constante_1.TILE_SIZE, constante_1.ALTO_VENTANA))
        pygame.draw.line(ventana, constante_1.BLANCO, (0, x * constante_1.TILE_SIZE), (constante_1.ANCHO_VENTANA, x * constante_1.TILE_SIZE))

jugador = Personaje(constante_1.ANCHO_VENTANA // 2, constante_1.ALTO_VENTANA // 2, animaciones, 100, 1)

# Configurar la posición fija de la torre en el mapa
torre_posicion_fija = (1800, 1000)
torre_imagen = pygame.image.load(f"assets//images//characters//Enemigos//{tipo_enemigos[1]}//{tipo_enemigos[1]}_1.png").convert_alpha()
torre_imagen = escalar_img(torre_imagen, constante_1.SCALA_ENEMIGOS)

# Crear objeto Torre
Torre = Personaje(torre_posicion_fija[0], torre_posicion_fija[1], [torre_imagen], 2000, 2)

# Añadir Torre a objetos_frame
objetos_frame["torre"] = Torre

Baculo = Weapon(imagen_Baculo, imagen_BLuz)
grupo_damage_text = pygame.sprite.Group()
grupo_BLuz = pygame.sprite.Group()

Mover_arriba = False
Mover_abajo = False
Mover_derecha = False
Mover_izquierda = False
Basico_1 = 25
reloj = pygame.time.Clock()
run = True

# Variables de desplazamiento del fondo
bg_scroll_x = 0
bg_scroll_y = 0

ajuste_x = 50
ajuste_y = 30

# Cargar la imagen del ataque básico (proporciona la ruta correcta)
ataqueEspecial21_img = pygame.image.load("assets/images/Weaponds/FireBool_2_1.png").convert_alpha()
ataqueEspecial21_img = escalar_img(ataqueEspecial21_img, constante_1.SCALA_ATAQUE_ESPECIAL21)

# Cargar la imagen del ataque especial básico (proporciona la ruta correcta)
ataqueEspecial11_img = pygame.image.load("assets/images/Weaponds/BolaMorada.png").convert_alpha()
ataqueEspecial11_img = escalar_img(ataqueEspecial11_img, constante_1.SCALA_ATAQUE_ESPECIAL11)

# Una bandera para indicar cuando el ataque está activo
ataque_basico_activo = False
ataque_especial_basico1_activo = False
ataque_especial_basico1_timer = 0  # Agregar temporizador para el ataque especial básico

# Variables de control de ataques
ataque_basico_activo = False
ataque_especial_basico1_activo = False
ataque_basico_timer = 0
ataque_especial_basico1_timer = 0

DURACION_ATAQUE_BASICO = 0.5  # Duración del ataque básico en segundos

while run:
    reloj.tick(constante_1.FPS)

    delta_x = 0
    delta_y = 0
    if Mover_derecha:
        delta_x = constante_1.VELOCIDAD
    if Mover_izquierda:
        delta_x = -constante_1.VELOCIDAD
    if Mover_arriba:
        delta_y = -constante_1.VELOCIDAD
    if Mover_abajo:
        delta_y = constante_1.VELOCIDAD

    if not (0 <= bg_scroll_x + delta_x <= MAP_WIDTH - constante_1.ANCHO_VENTANA):
        delta_x = 0
    if not (0 <= bg_scroll_y + delta_y <= MAP_HEIGHT - constante_1.ALTO_VENTANA):
        delta_y = 0

    jugador_rect_nuevo = jugador.forma.copy()
    jugador_rect_nuevo.x += delta_x
    jugador_rect_nuevo.y += delta_y

    colision = False
    for rect in rectangulos_arboles:
        rect.x -= bg_scroll_x
        rect.y -= bg_scroll_y
        if jugador_rect_nuevo.colliderect(rect):
            colision = True
        rect.x += bg_scroll_x
        rect.y += bg_scroll_y

    if not colision:
        bg_scroll_x += delta_x
        bg_scroll_y += delta_y

    for x in range(-bg_width, constante_1.ANCHO_VENTANA + bg_width, bg_width):
        for y in range(-bg_height, constante_1.ALTO_VENTANA + bg_height, bg_height):
            ventana.blit(background_image, (x - bg_scroll_x % bg_width, y - bg_scroll_y % bg_height))

    posicion_pantalla = jugador.movimiento(delta_x, delta_y)
    jugador.update()

    for pos in posiciones_arboles:
        ventana.blit(arbol_image, (pos[0] - bg_scroll_x, pos[1] - bg_scroll_y))

    ventana.blit(torre_imagen, (torre_posicion_fija[0] - bg_scroll_x, torre_posicion_fija[1] - bg_scroll_y))
    Torre.forma.topleft = (torre_posicion_fija[0] - bg_scroll_x, torre_posicion_fija[1] - bg_scroll_y)

    area_ataque_rect = pygame.Rect(
        torre_posicion_fija[0] - 200 - bg_scroll_x + ajuste_x, 
        torre_posicion_fija[1] - 200 - bg_scroll_y + ajuste_y, 
        400, 
        400
    )

    pygame.draw.rect(ventana, constante_1.ROJO, area_ataque_rect, 2)

    en_area_ataque = area_ataque_rect.colliderect(jugador.forma)

    tiempo_ahora = time.time()
    if ataque_especial:
        if tiempo_ahora - tiempo_ultimo_ataque_especial >= DURACION_ATAQUE_ESPECIAL or not en_area_ataque:
            ataque_especial = False
            Baculo.incremento_dano = 1
            print("El ataque especial ha terminado. Enfriamiento iniciado.")
    else:
        tiempo_restante_enfriamiento = TIEMPO_ENFIRAMIENTO - (tiempo_ahora - tiempo_ultimo_ataque_especial)
        if tiempo_restante_enfriamiento > 0:
            print(f"Tiempo de enfriamiento restante: {int(tiempo_restante_enfriamiento)} segundos")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Mover_izquierda = True
            if event.key == pygame.K_d:
                Mover_derecha = True
            if event.key == pygame.K_w:
                Mover_arriba = True
            if event.key == pygame.K_s:
                Mover_abajo = True
            if event.key == pygame.K_p and en_area_ataque and not ataque_especial:
                tiempo_ahora = time.time()
                if tiempo_ahora - tiempo_ultimo_ataque_especial >= TIEMPO_ENFIRAMIENTO:
                    ataque_especial = True
                    tiempo_ultimo_ataque_especial = tiempo_ahora
                    Baculo.incremento_dano = 2
                    print(f"Ataque especial activado. Durará {DURACION_ATAQUE_ESPECIAL} segundos.")

            # Ataque Especial Basico ("i")        
            if event.key == pygame.K_i:
                print("Ejecutando ataque básico...")
                avatar.ataqueEspecial21(objetos_frame)  
                ataque_basico_activo = True  
                ataque_basico_timer = time.time()

            # ATAQUE ESPECIAL BÁSICO ("u")
            if event.key == pygame.K_u:
                print("Ejecutando ataque especial básico 1...")
                avatar.ataqueEspecial11(objetos_frame)  
                ataque_especial_basico1_activo = True  
                ataque_especial_basico1_timer = time.time()  

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Mover_izquierda = False
            if event.key == pygame.K_d:
                Mover_derecha = False
            if event.key == pygame.K_w:
                Mover_arriba = False
            if event.key == pygame.K_s:
                Mover_abajo = False

    BLuz = Baculo.update(jugador)
    if BLuz:
        grupo_BLuz.add(BLuz)
    for BLuz in grupo_BLuz:
        damage, pos_damage = BLuz.update([Torre])
        if damage != 0:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constante_1.ROJO)
            grupo_damage_text.add(damage_text)

    grupo_damage_text.update()

    Baculo.dibujar(ventana)
    for BLuz in grupo_BLuz:
        BLuz.dibujar(ventana)
    grupo_damage_text.draw(ventana)


        # DIBUJAR ATAQUE BÁSICO SI ESTÁ ACTIVO
    if ataque_basico_activo:
        ventana.blit(
            ataqueEspecial21_img, 
            (jugador.forma.centerx - ataqueEspecial21_img.get_width() // 2, 
            jugador.forma.centery - ataqueEspecial21_img.get_height() // 2)
        )

    # Validar tiempo de ataque básico
    if ataque_basico_activo and time.time() - ataque_basico_timer > DURACION_ATAQUE_BASICO:
        ataque_basico_activo = False

    # Validar tiempo de ataque especial básico
    if ataque_especial_basico1_activo and time.time() - ataque_especial_basico1_timer > DURACION_ATAQUE_ESPECIAL:
        ataque_especial_basico1_activo = False


    # DIBUJAR ATAQUE ESPECIAL BÁSICO SI ESTÁ ACTIVO
    if ataque_especial_basico1_activo:
        ventana.blit(
            ataqueEspecial11_img, 
            (jugador.forma.centerx - ataqueEspecial11_img.get_width() // 2, 
            jugador.forma.centery - ataqueEspecial11_img.get_height() // 2)
        )


    jugador.dibujar(ventana)

    pygame.display.update()

pygame.quit()
