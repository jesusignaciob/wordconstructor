# -*- coding: utf-8 -*-

"""
    This file is part of El Rostro Humano.

    El Rostro Humano is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    El Rostro Humano is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with El Rostro Humano.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *

class Letra:
  def __init__(self):
    self.id = 0

    self.nombre = ""
    self.texto = ""
    self.activo = False
    
    self.fiducial_pos_x = 0
    self.fiducial_pos_y = 0
    
  def __init__(self, id, nombre, texto, imagen, sonido):
    self.id = id

    self.nombre = nombre
    self.texto = texto
    
    self.__rect = self.imagen.get_rect()
    self.__rect.centerx = x
    self.__rect.centery = y
    
    self.fiducial_pos_x = 0
    self.fiducial_pos_y = 0
    
    self.activo = False
    
  def __init__(self, nombre, configuracion):
    self.id = configuracion[nombre]['id']
    
    self.nombre = nombre
    self.texto = configuracion[nombre]['texto']
    
    self.fiducial_pos_x = 0
    self.fiducial_pos_y = 0
    
    self.activo = False
    
class Palabra:
  def __init__(self):
    self.nombre = ""
    self.texto = ""
    self.activo = False
    
    self.imagen = None
    self.sonido = None
    
  def __init__(self, x, y, w, h, nombre, texto, imagen, sonido):
    self.nombre = nombre
    self.texto = texto
    self.activo = False
    
    self.imagen = self.__load_image(imagen, w, h, False)
    self.sonido = pygame.mixer.Sound(sonido)
    
    self.__rect = self.imagen.get_rect()
    self.__rect.centerx = x
    self.__rect.centery = y
    
    self.activo = False
    
  def __init__(self, x, y, w, h, nombre, configuracion):
    self.nombre = nombre
    self.texto = configuracion[nombre]['texto']
    
    archivo_imagen = '%s/%s' % (configuracion['directorio_imagenes'], configuracion[nombre]['imagen'])
    self.imagen = self.__load_image(archivo_imagen, w, h, False)
    
    archivo_sonido = '%s/%s' % (configuracion['directorio_sonidos'], configuracion[nombre]['sonido'])
    self.sonido = pygame.mixer.Sound(archivo_sonido)
    
    self.__rect = self.imagen.get_rect()
    self.__rect.centerx = x
    self.__rect.centery = y
    
    self.activo = False
    
  def __scaleit(self, filename, w, h):
    i = pygame.image.load(filename)

    #if hasattr(pygame.transform, "smoothscale"):
    #  scaled_image = pygame.transform.smoothscale(i, (w,h))
    #else:
    #  scaled_image = pygame.transform.scale(i, (w,h))
    scaled_image = pygame.transform.scale(i, (w,h))
    
    return scaled_image

  def __load_image(self, filename, w, h, transparent=False):
    try: image = self.__scaleit(filename, w, h)
    except pygame.error, message:
      raise SystemExit, message
    image = image.convert()
    if transparent:
      color = image.get_at((0,0))
      image.set_colorkey(color, RLEACCEL)
    return image
    
  def mostrar(self, screen):
    screen.blit(self.imagen, self.__rect)
    
  def reproducir_sonido(self):
    return self.sonido.play()