import tkinter.messagebox as messagebox

class Overflow:
    def __init__(self):
        self.valor = int

    def operacion(self):
        try:
            resultado = self.valor ** 999999
            return resultado
        except OverflowError:
            messagebox.showerror("Error Overflow", "Error Overflow (Cantidad demasiado grande)")

    def establecer_valor(self, valor):
        self.valor = valor
        