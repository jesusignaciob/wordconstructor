#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Constructor de palabras
    Copyright (C) 2012 Jesús Becerra

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
import sys

import simplejson as json

import tuio
tracking = tuio.Tracking()

from tuio.objects import Tuio2DObject

from palabra import Palabra, Letra
from utilidades import *

def main():
  configuracion = cargarConfiguracion("config.json")
  config_letras = cargarConfiguracion("letras.json")
  config_palabras = cargarConfiguracion("palabras.json")
  
  SCREEN_WIDTH = configuracion['resolucion_horizontal']
  SCREEN_HEIGHT = configuracion['resolucion_vertical']

  posicion = Posicion(SCREEN_WIDTH, SCREEN_HEIGHT)
  
  directorio_imagenes = configuracion['directorio_imagenes']
  directorio_sonidos = configuracion['directorio_sonidos']
  
  pygame.init()
  pygame.mixer.init()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Constructor de Palabras")
  pygame.display.set_icon(pygame.image.load('%s/%s' % (directorio_imagenes, 'mono.jpg')))

  blanco = (255,255,255)
  rojo = (255,0,0)
  screen.fill(blanco)
  
  resolucion_horizontal_imagenes = configuracion['resolucion_horizontal_imagenes']
  resolucion_vertical_imagenes = configuracion['resolucion_vertical_imagenes']
  
  letras = cargarLetras(config_letras)
  print letras  
  palabras = cargarPalabras(_configuracion = config_palabras, \
                            _x = posicion.CENTRADO_HORIZONTAL(), \
                            _y = posicion.CENTRADO_VERTICAL(), \
                            _w = resolucion_horizontal_imagenes, \
                            _h = resolucion_vertical_imagenes, \
                            dir_imag = directorio_imagenes, \
                            dir_son = directorio_sonidos)
  print palabras
  
  # Define el tamaño de letra por defecto
  fuente = pygame.font.Font(None, 26)
  
  pygame.mixer.music.load('%s/%s' % (directorio_sonidos,'storybook.wav'))
  
  objetos_actuales = {}
  objeto_actual = Tuio2DObject(-1, -1)
  duracion = 0
  sound = None
  channel = None
  clock = pygame.time.Clock()

  pygame.mixer.music.play(-1)

  while True:
    screen.fill(blanco)
    
    tracking.update()
    tuio_obj_actual = Tuio2DObject(-1, -1)
    
    for obj in tracking.objects():
      tuio_obj_actual = obj
      disponible = True #por defecto el canal esta disponible
      haveChannel = sound <> None #Se tiene un canal asociado
      disponible = True #por defecto el canal esta disponible
      
      """
      Si el fiducial asociado es el asociado a la letra la añade a la lista
      """
      for letra in letras:
        if letra.id == obj.id:
          objetos_actuales[obj.xpos] = letra.texto
    
    palabra_en_diccionario = objetos_actuales.copy()
    objetos_actuales = {}
    
    """
    Verifica si se tienen ambas figuras del ojo simultaneamente con esto se reproduce un sonido diferente (ojos)
    """
    if len(palabra_en_diccionario) > 0:
      duracion += clock.tick()
      
      palabra_claves_ordenado = sorted(palabra_en_diccionario)
      
      palabra_string = ''
      for clave in palabra_claves_ordenado:
        palabra_string += palabra_en_diccionario[clave]
      
      palabra_string = palabra_string.upper()
      
      mensaje = fuente.render(palabra_string, 1, (0, 0, 0))
      screen.blit(mensaje, (posicion.CENTRADO_HORIZONTAL(), 15))
      
      if duracion > 5000:

        for palabra in palabras:
          if palabra.texto.upper() == palabra_string:
            print "Palabra: %s" % palabra_string
            palabra.mostrar(screen)
            if sound <> palabra.sonido:
              if haveChannel: #Si se tiene un canal asociado
                """
                Si el canal no esta reproduciendo un sonido significa que esta disponible
                """
                disponible = not channel.get_busy()
              
              if disponible: #Si el canal esta disponible
                sound = palabra.sonido #Se actualiza el mixer con el nuevo sonido
                channel = sound.play() #Se manda a reproducir y guarda el canal
        
    else: 
      duracion = 0
    
    palabra_en_diccionario = {}
    
    """
    Si no se encuentra actualmente un objeto en camara cancela cualquier sonido
    que se encuentre actualmente en ejecución
    """
    if tuio_obj_actual.id == -1:
      if sound <> None:
        sound.stop()
      sound = None
    
    pygame.display.flip()
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
	  sys.exit()

if __name__ == "__main__":
  main()
