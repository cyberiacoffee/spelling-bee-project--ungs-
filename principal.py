#! /usr/bin/env python
import os, random, sys, math

import pygame
from pygame.locals import *

from configuracion import *
from funcionesVACIAS import *
from extras import *

#Funcion principal

def main():
        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        #Preparar la ventana
        pygame.display.set_caption("Spelling Bee!") ##Le agrega el nombre al juego
        screen = pygame.display.set_mode((ANCHO, ALTO))
        fondo= pygame.image.load('fondo.png') ##Le agregamos fondo
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        screen.blit(fondo,[0, 0])
        pygame.display.flip()

        #Agregar icono
        icono = pygame.image.load('icono.jpg')
        pygame.display.set_icon(icono)

        #Agregar musica y sonidos
        musica=pygame.mixer.music.load('musica_fondo.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        palabraCorrecta = pygame.mixer.Sound("sonido_correcto.mp3")
        palabraIncorrecta= pygame.mixer.Sound("sonido_error.mp3")


        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial

        #se definen variables necesarias
        puntos = 0
        candidata = ""
        diccionario = []
        palabrasAcertadas = []

        #lee el diccionario
        diccionario=lectura(diccionario)


        #elige las 7 letras al azar y una de ellas como principal
        letrasEnPantalla = dame7Letras()
        letraPrincipal = dameLetra(letrasEnPantalla)

        #se queda con 7 letras que permitan armar muchas palabras, evita que el juego sea aburrido
        while(len(dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario))< MINIMO):
            letrasEnPantalla = dame7Letras()
            letraPrincipal = dameLetra(letrasEnPantalla)

        print(dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario))

        #dibuja la pantalla la primera vez
        dibujar(screen, letraPrincipal, letrasEnPantalla, candidata, puntos, segundos, palabrasAcertadas)

        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
            	fps = 3

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    candidata += letra   #va concatenando las letras que escribe
                    if e.key == K_BACKSPACE:
                        candidata = candidata[0:len(candidata)-1] #borra la ultima
                    if e.key == K_RETURN:  #presionó enter
                        if candidata not in palabrasAcertadas:
                            puntos += procesar(letraPrincipal, letrasEnPantalla, candidata, diccionario,palabraCorrecta,palabraIncorrecta)
                            if esValida(letraPrincipal, letrasEnPantalla, candidata, diccionario): ##si la palabra es valida la guarda en la lista palabrasAcertadas
                                palabrasAcertadas.append(candidata)
                        candidata = ""

            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)
            screen.blit(fondo,[0, 0])

            #Dibujar de nuevo todo
            dibujar(screen, letraPrincipal, letrasEnPantalla, candidata, puntos, segundos, palabrasAcertadas)

            pygame.display.flip()

        nombre=ingresarUsuario(screen) #Crea una pantalla para que el usuario ingrese su nombre y lo guarda
        pantallaGameOver(screen, palabrasAcertadas, puntos) #Muestra la pantalla de game over con las palabras acertadas y los puntos
        guardarPuntajes(nombre, puntos) #si el puntaje esta entre los mejores 10, guarda el puntaje junto con el nombre del usuario en el documento de texto
        mejoresPuntajes(screen) #muestra los 10 mejores puntajes


        while 1: #En la pantalla final, se debe presionar enter para salir del juego
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        return

#Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
