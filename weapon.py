import pygame
from pygame.sprite import Group
import constante_1
import math
import random

class Weapon(): 
    def __init__(self, image, imagen_BLuz):
        self.imagen_BLuz = imagen_BLuz
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.dispara = False
        self.ultimo_disparo = pygame.time.get_ticks()
        self.incremento_dano = 1  # Variable para controlar el aumento del daño

    def update(self, personaje):
        disparo_cooldown = constante_1.COOLDOWN_BLuz
        BLuz = None
        self.forma.center = personaje.forma.center
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width / 2.1
            self.rotar_arma(False)
        if personaje.flip == True:
            self.forma.x = self.forma.x - personaje.forma.width / 2.1
            self.rotar_arma(True)
        self.forma.y = self.forma.y + -0.3

        # Mover Baculo con Mause
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        # Detectar balas/golpes con mouse 
        if pygame.mouse.get_pressed()[0] and self.dispara == False and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            BLuz = Bullet(self.imagen_BLuz, self.forma.centerx, self.forma.centery, self.angulo, self.incremento_dano)
            self.ultimo_disparo = pygame.time.get_ticks()
            self.dispara = True

        # Resetear click del mouse 
        if pygame.mouse.get_pressed()[0] == False:
            self.dispara = False 
        return BLuz

    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, ventana):
        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        ventana.blit(self.imagen, self.forma)
        # pygame.draw.rect(ventana, constante_1.COLOR_ARMA, self.forma, 1) --> Podemos ver las dimensiones del Baculo

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, incremento_dano):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.incremento_dano = incremento_dano

        # Calculo de la velocidad de disparo
        self.delta_x = math.cos(math.radians(self.angulo)) * constante_1.VELOCIDAD_BLuz
        self.delta_y = -math.sin(math.radians(self.angulo)) * constante_1.VELOCIDAD_BLuz
    
    def update(self, lista_enemigos):
        daño = 0
        pos_daño = None
        self.rect.x += self.delta_x
        self.rect.y = self.rect.y + self.delta_y

        # BLuz Fuera de pantalla 
        if self.rect.right < 0 or self.rect.left > constante_1.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > constante_1.ALTO_VENTANA:
            self.kill()

        # Verificacion de colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = (100 + random.randint(-25, 20)) * self.incremento_dano  # Aplicar el incremento del daño
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break

        return daño, pos_daño

    def dibujar(self, ventana):
        ventana.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height())))
