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


unaFunc(5, "hola")
unaFunc(7, "juan",False)
unaFunc(9,"laura","pedro")
unaFunc()
unaFunc(False)
