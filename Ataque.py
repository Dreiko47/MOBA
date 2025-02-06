/Como generar un ataque que detecte colisiones e imprima en la interfaz grafica de pygame el daño generado.

/Se deben definir variables con los diferentes valores que tendran cada uno de estos: iniciacion, posicion, duracion, regeneracion, etc...

----------Ejemplo----------

ataque_explosion_activo = False
ataque_explosion_timer = 0
DURACION_ATAQUE_EXPLOSION = 0.5  # Duración del ataque de explosión en segundos
TIEMPO_ENFRIAMIENTO_EXPLOSION = 60  # Tiempo de enfriamiento para el ataque de explosión en segundos
tiempo_ultimo_ataque_explosion = 0


Para generar una imagen que represente este ataque, colocaremos su direccion donde cargamos las imagenes.

----------Ejemplo----------

# Cargar la imagen del nuevo ataque (explosión)
ataqueExplosion_img = pygame.image.load("assets/images/Weaponds/FireBool_2_1.png").convert_alpha()
ataqueExplosion_img = escalar_img(ataqueExplosion_img, constante_1.SCALA_ATAQUE_EXPLOSION)



/Tambien debemos asignar una tecla o botton con el que se ejecutara el ataque, para este ejemplo se utilizo la letra "E", junto con las propidades del ataque
como el daño, si el daño sera variable, el momento en que se activara el ataque, el tiempo donde se toma la nueva inicializacion y algunas reglas que queramos
ejecutar.


----------Ejemplo----------


# Activar el ataque de explosión con la tecla "e" si el jugador está dentro del área de ataque y ha pasado el tiempo de enfriamiento
            if event.key == pygame.K_e and en_area_ataque:
                tiempo_ahora = time.time()
                if tiempo_ahora - tiempo_ultimo_ataque_explosion >= TIEMPO_ENFRIAMIENTO_EXPLOSION:
                    print("Ejecutando ataque de explosión...")
                    ataque_explosion_activo = True
                    ataque_explosion_timer = tiempo_ahora
                    tiempo_ultimo_ataque_explosion = tiempo_ahora
                    damage_base = 250  # Daño causado por la explosión
                    damage_variacion = random.randint(-10, 10)
                    damage = damage_base + damage_variacion
                    Torre.recibir_dano(damage)
                   
                    damage_text = DamageText(Torre.forma.centerx, Torre.forma.centery, str(damage), font, constante_1.ROJO)
                    grupo_damage_text.add(damage_text)
                    print(f"Ataque de explosión causó {damage} de daño a la torre.")
                else:
                    tiempo_restante_enfriamiento = int(TIEMPO_ENFRIAMIENTO_EXPLOSION - (tiempo_ahora - tiempo_ultimo_ataque_explosion))
                    print(f"El ataque de explosión está en enfriamiento. Tiempo restante: {tiempo_restante_enfriamiento} segundos")



/Ahora se debe considerar la parte donde vamos a dibujar el daño realizado al objetivo, esto para imprimirlo en la interfaz garfica de pygame
al igual que la posicion donde aparecera el texto del daño en la torre. 
  

----------Ejemplo----------
  
        # DIBUJAR ATAQUE DE EXPLOSIÓN SI ESTÁ ACTIVO
    if ataque_explosion_activo:
        ventana.blit(
            ataqueExplosion_img, 
            (jugador.forma.centerx - ataqueExplosion_img.get_width() // 2, 
            jugador.forma.centery - ataqueExplosion_img.get_height() // 2)
        )

    # Validar tiempo de ataque de explosión
    if ataque_explosion_activo and time.time() - ataque_explosion_timer > DURACION_ATAQUE_EXPLOSION:
        ataque_explosion_activo = False


