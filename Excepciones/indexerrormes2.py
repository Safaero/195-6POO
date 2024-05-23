class Mes:
    def __init__(self):
        self.meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio",
                      "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")

    def obtener_nombre(self, numero):
        return self.meses[numero - 1]