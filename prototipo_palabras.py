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

class Posicion:
  def __init__(self):
    self.screen_width = 0
    self.screen_height = 0
    
  def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
    self.screen_width = SCREEN_WIDTH
    self.screen_height = SCREEN_HEIGHT
  
  def CENTRADO_HORIZONTAL(self):
    return self.screen_width/2
    
  def CENTRADO_VERTICAL(self):
    return self.screen_height/2
    
  def TERCIO_HORIZONTAL(self):
    return self.screen_width/4

def cargarConfiguracion(archivo):
  fconfig = open(archivo, "r")
  configuracion = "";
  
  while True:
      linea = fconfig.readline()
      if not linea: break
      configuracion += linea
  
  return json.loads(configuracion)

def main():
  configuracion = cargarConfiguracion(archivo = "config.json")
  palabras = cargarConfiguracion(archivo = "bd.json")
  
  SCREEN_WIDTH = configuracion['resolucion_horizontal']
  SCREEN_HEIGHT = configuracion['resolucion_vertical']

  posicion = Posicion(SCREEN_WIDTH, SCREEN_HEIGHT)

  objetos_actuales = []
  
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

  letra_A = Letra(nombre = 'letra_A', configuracion = configuracion)
  letra_M = Letra(nombre = 'letra_M', configuracion = configuracion)
  letra_N = Letra(nombre = 'letra_N', configuracion = configuracion)
  letra_O = Letra(nombre = 'letra_O', configuracion = configuracion)
  
  mano = Palabra(x = posicion.CENTRADO_HORIZONTAL(), y = posicion.CENTRADO_VERTICAL(), w = 140, h = 140, nombre = "mano", configuracion = palabras)
  no = Palabra(x = posicion.CENTRADO_HORIZONTAL(), y = posicion.CENTRADO_VERTICAL(), w = 140, h = 140, nombre = "no", configuracion = palabras)
  
  # Define el tamaño de letra por defecto
  fuente = pygame.font.Font(None, 26)
  
  pygame.mixer.music.load('%s/%s' % (directorio_sonidos,'storybook.wav'))
  
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
      if tuio_obj_actual.id <> obj.id:
        objeto_actual = obj
        
      tuio_obj_actual = obj
      disponible = True #por defecto el canal esta disponible
      haveChannel = sound <> None #Se tiene un canal asociado
      disponible = True #por defecto el canal esta disponible
      
      """
      Si el fiducial asociado es el asociado a la vocal A (idA) dibuja la imagen de la vocal
      y ejecuta el sonido referente a este siempre y cuando no se tenga otro sonido en ejecución 
      """
      if letra_A.id == objeto_actual.id:
        if not letra_A.activo:
          objetos_actuales.append(letra_A.texto)
          letra_A.activo = True
        
      elif letra_M.id == objeto_actual.id:
        if not letra_M.activo:
          objetos_actuales.append(letra_M.texto)
          letra_M.activo = True
        
      elif letra_N.id == objeto_actual.id:
        if not letra_N.activo:
          objetos_actuales.append(letra_N.texto)
          #print 'Agrego %s' % letra_N.texto
          letra_N.activo = True
        
      elif letra_O.id == objeto_actual.id:
        if not letra_O.activo:
          objetos_actuales.append(letra_O.texto)
          #print 'Agrego %s' % letra_O.texto
          letra_O.activo = True
      
      objeto_actual = Tuio2DObject(-1, -1)
    
    """
    Verifica si se tienen ambas figuras del ojo simultaneamente con esto se reproduce un sonido diferente (ojos)
    """
    if len(objetos_actuales) > 0:
      duracion += clock.tick()
      
      if duracion > 5000:
        letras = ''.join(objetos_actuales)
        
        mensaje = fuente.render(letras, 1, (0, 0, 0))
        screen.blit(mensaje, (posicion.CENTRADO_HORIZONTAL(), 15))
        
        if mano.texto == letras:
          print "Palabra: %s" % letras
          mano.mostrar(screen)
          if sound <> mano.sonido:
            if haveChannel: #Si se tiene un canal asociado
              """
              Si el canal no esta reproduciendo un sonido significa que esta disponible
              """
              disponible = not channel.get_busy()
            
            if disponible: #Si el canal esta disponible
              sound = mano.sonido #Se actualiza el mixer con el nuevo sonido
              channel = sound.play() #Se manda a reproducir y guarda el canal
            
        elif no.texto == letras:
          print "Palabra: %s" % letras
          no.mostrar(screen)
          if sound <> no.sonido:
            if haveChannel: #Si se tiene un canal asociado
              """
              Si el canal no esta reproduciendo un sonido significa que esta disponible
              """
              disponible = not channel.get_busy()
            
            if disponible: #Si el canal esta disponible
              sound = no.sonido #Se actualiza el mixer con el nuevo sonido
              channel = sound.play() #Se manda a reproducir y guarda el canal
        
    else: 
      duracion = 0
      letra_N.activo = False
      letra_O.activo = False
          
    """
    Si no se encuentra actualmente un objeto en camara cancela cualquier sonido
    que se encuentre actualmente en ejecución
    """
    if tuio_obj_actual.id == -1:
      objetos_actuales = []
      if sound <> None:
        sound.stop()
      sound = None
    
    pygame.display.flip()
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
	  sys.exit()

if __name__ == "__main__":
  main()
