class Mes:
    def __init__(self):
        self.meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio",
                      "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")

    def obtener_nombre(self, numero):
        try:
            if 1 <= numero <= 12:
                return self.meses[numero - 1]
            else:
                return "El número debe estar entre 1 y 12"
        except IndexError:
            return "El número debe estar entre 1 y 12"
