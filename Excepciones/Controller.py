class ExcepcionEdadInvalida(Exception):
    def __init__(self, edad, mensaje="La edad ingresada es menor a 18"):
        self.edad = edad
        self.mensaje = mensaje
        super().__init__(self.mensaje)
        print("La edad introducida fue",edad)

class ExcepcionNombre(Exception):
    def __init__(self, mensaje="El nombre no se encontro en la lista"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class Controller:
    
    lista = ["emiliano"]

    def verificarEdadCont(self,edad):
        
        if edad < 18:
            raise ExcepcionEdadInvalida(edad)
        else:
            return 1
    
    
    def buscarNombre(self,nombre):
        
        if nombre in self.lista:
            return 1
        else:
            raise ExcepcionNombre
        
        