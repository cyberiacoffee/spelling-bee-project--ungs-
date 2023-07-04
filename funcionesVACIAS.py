from principal import *
from configuracion import *
import random
import math
import time


def lectura(diccionario): ##Lee el diccionario y lo guarda en forma de lista
  lista=[]
  diccionarioCargado = open("lemario.txt", "r", encoding='latin1')
  for linea in diccionarioCargado:
    linea=linea[:-1]
    lista.append(linea)
  return lista

def dame7Letras(): ##nos retorna una cadena compuesta por una consonante dificil, cuatro consonantes normales y dos vocales
    vocales=["a","e","i","o","u"] ##para facilitar la elección de las letras creamos una lista para cada categoria
    consonanteDificil = ["k", "x", "y", "z","w"]
    consonante=["b", "c", "d", "f", "g", "h","j", "l", "m", "n", "p", "q", "r", "s", "t", "v"]
    lista="".join(random.sample(consonanteDificil,1)+random.sample(vocales,2)+random.sample(consonante,4)) ##usando el .join(random.sample(LISTA,PARAMETRO)) le damos la lista a utilizar y la cantidad de letras a concatenar en la cadena llamada lista
    return lista


def dameLetra(letrasEnPantalla): ##recibe una cadena con las letras recibidas de la funcion dame7Letras(), elije una de estas y la retorna
  return letrasEnPantalla[random.randint(0,6)]



def esValida(letraPrincipal, letrasEnPantalla, candidata, diccionario): ##Verifica que la palabra ingresada contenga la letra principal, solo este compuesta por letras en pantalla y que exista en el lemario
    return letraPrincipal in candidata and set(candidata).issubset(letrasEnPantalla) and candidata in diccionario



def Puntos(candidata): ##recibe la palabra candidata y teniendo en cuenta la longitud de esta determina cuantos puntos se retornan
  if len(candidata)<3:
    puntos=-1

  elif len(candidata)==3:
    puntos=1

  elif len(candidata)==4:
    puntos=2

  elif len(candidata)==5:
   puntos=5

  elif len(candidata)==6:
    puntos=6

  elif len(candidata)>=7:
    puntos=10

  return puntos



def procesar(letraPrincipal, letrasEnPantalla, candidata, diccionario,palabraCorrecta,palabraIncorrecta): ##usa la función esValida, si esta retorna True, retorna los puntos usando la variable Puntos, si retorna False, esta retorna -1
  if esValida(letraPrincipal, letrasEnPantalla, candidata, diccionario):
    palabraCorrecta.play() ##si la palabra ingresada es correcta reproduce un sonido de OK
    return Puntos(candidata)
  else:
    palabraIncorrecta.play() ## lo mismo que arriba pero si es incorrecta
    return -1


def dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario):
    diccionario = open("lemario.txt", "r", encoding='latin1') ##pone el diccionario en modo lectura
    listaPalabras = [] ##creamos dos listas a utilizar
    listaFinal=[]
    for linea in diccionario: ##recorre el diccionario linea por linea y guarda la linea en la variable palabra, si la palabra contiene la letra principal guarda la palabra en listaPalabras
        palabras = linea.split()
        for palabra in palabras:
            if letraPrincipal in palabra:
                listaPalabras.append(palabra)

    for cadena in listaPalabras:
        letrasValidas = set(letrasEnPantalla)
        if set(cadena).issubset(letrasValidas) and len(cadena)>=3 :
            listaFinal.append(cadena)
    return listaFinal


def pantallaGameOver(screen, palabrasAcertadas, puntos): ##Crea una pantalla de game over donde se muestran las palabras acertadas ordenadas alfabeticamente y los puntos obtenidos

    fondo= pygame.image.load('final.png') ## se cargan los datos correspondientes
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    screen.blit(fondo,[0, 0])
    pygame.display.flip()

    ruta_fuente = os.path.join("minecraft.ttf")

    defaultFont = pygame.font.Font(ruta_fuente, 30)
    defaultFont2= pygame.font.Font(ruta_fuente, 20)

    # Mostrar "Game Over"
    ren1 = defaultFont.render("Game Over", 1, (255, 0, 0))
    screen.blit(ren1, (ANCHO // 2 - ren1.get_width() // 2, 30))

    # Mostrar palabras acertadas ordenadas por letra inicial
    ren2 = defaultFont.render("Palabras acertadas:", 1, COLOR_TEXTO)
    screen.blit(ren2, (ANCHO // 2 - ren2.get_width() // 2, 70))


    y_pos = 110
    if len(palabrasAcertadas)>0:
        palabrasAcertadas.sort()  # Ordenar palabras acertadas alfabéticamente
        for i, palabra in enumerate(palabrasAcertadas):
            texto_palabra = defaultFont2.render(palabra, 1, (0,0,0))
            screen.blit(texto_palabra, (ANCHO // 2 - texto_palabra.get_width() // 2, y_pos + i * 20))
    elif len(palabrasAcertadas)==0:
        texto_palabra = defaultFont2.render(":(", 1, (255, 255, 0))
        screen.blit(texto_palabra, (ANCHO // 2 , y_pos))

    ## Mostrar puntaje total

    if puntos>0:
        ren3 = defaultFont.render("Puntaje total: " + str(puntos), 1, COLOR_TEXTO)
        screen.blit(ren3, (ANCHO // 2 - ren3.get_width() // 2, 550))
    else:
        ren3 = defaultFont.render("Puntaje total: " + str(puntos), 1, (255, 0, 0))
        screen.blit(ren3, (ANCHO // 2 - ren3.get_width() // 2, 550))

    pygame.display.flip()

    pygame.time.delay(5000) ##Hace que la pantalla de game over se muestre durante 5 segundos y luego pase a la siguiente funcion

    return

def guardarPuntajes(nombre, puntos): ##Lee el documento de texto de records, agrega el nuevo record, los ordena de mayor a menor y deja solo los mejores 10
    puntajes = []

    with open('records.txt', 'r') as archivo:
        for linea in archivo:
            registro = linea.strip().split(',')
            puntajes.append(registro)

    puntajes.append([nombre, str(puntos)])  ## Agrega nuevo puntaje a la lista de puntajes

    puntajes_ordenados = sorted(puntajes, key=lambda x: int(x[1]), reverse=True)
    puntajes_ordenados = puntajes_ordenados[:10]

    with open('records.txt', 'w') as archivo:
        for registro in puntajes_ordenados:
            archivo.write(','.join(registro) + '\n')

def mejoresPuntajes(screen): ##Muestra en pantalla los 10 mejores puntajes
    puntajes = []
    with open('records.txt', 'r') as archivo:
        for linea in archivo:
            registro = linea.strip().split(',')
            puntajes.append(registro)

    ruta_fuente = os.path.join("minecraft.ttf")
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mejores Puntajes")

    fondo = pygame.image.load('fondo_records.png')
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    screen.blit(fondo, [0, 0])
    pygame.display.flip()

    defaultFont = pygame.font.Font(ruta_fuente, 30)
    defaultFont2 = pygame.font.Font(ruta_fuente, 20)

    ren1 = defaultFont.render("Mejores Records:", 1, (255, 255, 0))
    screen.blit(ren1, (ANCHO // 2 - ren1.get_width() // 2, 30))

    y_pos = 100
    for i in range(len(puntajes)):
        texto_palabra = defaultFont.render(', '.join(puntajes[i]), 1, (220,220,220))
        screen.blit(texto_palabra, (ANCHO // 2 - texto_palabra.get_width() // 2, y_pos + i * 30))
    pygame.display.flip()

    ren2 = defaultFont.render("PRESIONE ENTER PARA CERRAR EL JUEGO", 1, (255, 0, 0)) ## al finalizar el  juego, se debe presionar ENTER para cerrar el juego
    screen.blit(ren2, (ANCHO // 2 - ren2.get_width() // 2, 550))
    pygame.display.flip()



def ingresarUsuario(screen):
    username = ""
    ruta_fuente = os.path.join("minecraft.ttf")
    defaultFont = pygame.font.Font(ruta_fuente, 36)
    teclasActivas = True
    screen = pygame.display.set_mode((ANCHO, ALTO))

    while teclasActivas: ##Mientras haya actividad en el teclado
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  ## Al presionar Enter, se termina la entrada
                    teclasActivas = False
                elif event.key == pygame.K_BACKSPACE:  ## Al presionar Retroceso, se borra el último caracter
                    username = username[:-1]
                else:
                    username += event.unicode ##Se carga en la variable username el input activo del teclado

        fondo = pygame.image.load('fondo_usuario.png')
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        screen.blit(fondo, [0, 0])
        aviso = defaultFont.render("Ingresa tu nombre de usuario:", True, (0,0,0))
        screen.blit(aviso, (ANCHO // 2 - aviso.get_width() // 2, ALTO // 2 - 50))

        inputUsuario = defaultFont.render(username, True, (0,0,0))
        screen.blit(inputUsuario, (ANCHO // 2 - inputUsuario.get_width() // 2, ALTO // 2))

        pygame.display.flip()

    return username
