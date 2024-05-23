from tkinter import messagebox

class Calculadora:
    def __init__(self, numero1, numero2):
        self.numero1 = numero1
        self.numero2 = numero2
        
    def division(self):
        try:
            resultado = self.numero1 / self.numero2
            return resultado
        except ZeroDivisionError:
            messagebox.showerror('Error', 'No se puede dividir entre 0')