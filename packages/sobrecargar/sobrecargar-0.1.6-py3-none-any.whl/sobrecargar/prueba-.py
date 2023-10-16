
from inspect import signature
from typing import NamedTuple
from collections import namedtuple
from sobrecargar import sobrecargar

@sobrecargar
def a(x:int,y: str, z:bool =False) -> str : pass

sig = signature(a)

for a,b in sig.parameters.items():
    print(f"{a}->{b}")
    print(f"{b.kind}")

Puntaje : NamedTuple = namedtuple('Puntaje', ['largoExacto','largoVar','largoDefecto','tipos'])


print(f"{d>c=}")

"""
from sobrecargar import overload

@overload
def unaFunc(x : int, y : str, z: bool = False):
    print(f"firma 1. {x=},{y=}, z por defecto = False, {z=}")


@overload
def unaFunc(x : int, y : str, z: str = None):
    
    cierreCadena = "no hubo flag seteada"   if z is None else f"{z=}"
    print(f"firma 2. {x=},{y=}, {cierreCadena}")

@overload 
def unaFunc(x : bool = True):
    cadena = f"es verdadero" if x else "es falso"
    print(f"firma 3. {cadena}")


unaFunc(5, "hola",None)

unaFunc(7, "juan",False)
unaFunc(9,"laura","pedro")
unaFunc()
unaFunc(False)
"""