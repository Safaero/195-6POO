import tkinter as tk
from Clase import *

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("OverflowError")

        self.manejador = Overflow()

        self.label = tk.Label(root, text="Ingrese un número:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button_calcular = tk.Button(root, text="Calcular", command=self.calcular)
        self.button_calcular.pack()

        self.resultado = tk.Label(root, text="")
        self.resultado.pack()

    def calcular(self):
        try:
            valor = float(self.entry.get())
            self.manejador.establecer_valor(valor)
            resultado = self.manejador.operacion()
            self.resultado.config(text=str(resultado))
        except ValueError:
            self.resultado.config(text="Error: Ingrese un número válido")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()