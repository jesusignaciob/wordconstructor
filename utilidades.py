# -*- coding: utf-8 -*-

"""
    This file is part of Constructor de Palabras.

    El Rostro Humano is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    El Rostro Humano is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Constructor de Palabras.  If not, see <http://www.gnu.org/licenses/>.
"""

import simplejson as json
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
  
def cargarPalabras(_configuracion, _x = 0, _y = 0, _w = 140, _h = 140, dir_imag = '', dir_son = ''):
  _palabras = []
  
  for k, v in _configuracion.iteritems():
    palabra = Palabra(x = _x, y = _y, w = _w, h = _h, nombre = k, directorio_imagenes = dir_imag, directorio_sonidos = dir_son, configuracion = _configuracion)
    _palabras.append(palabra)
    
  return _palabras
  
def cargarLetras(_configuracion):
  _letras = []
  
  for k, v in _configuracion.iteritems():
    letra = Letra(nombre = k, configuracion = _configuracion)
    _letras.append(letra)
    
  return _letras