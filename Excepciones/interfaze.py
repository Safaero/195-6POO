from Calculadora import *
from tkinter import messagebox
import tkinter as tk

class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Division')
        self.ventana.geometry('300x200')
        
        disenoTitulo = ('Arial',15,'bold')
        disenoTexto = ('Arial',12)
        disenoLabel = {'font':disenoTitulo, 'fg':'blue'}
        disenoimput = {'font':disenoTexto, 'fg': 'black'}
        disenoBoton = {'font':('Arial',12,'bold'),'bg':'green','fg':'white'}  
        
        info = 'Calculadora de divisiones' 
        self.labelInfo = tk.Label(ventana, text=info, font=disenoTitulo)
        self.labelInfo.pack()
        
        self.Labelnumero1 = tk.Label(ventana, text='Divisor:')
        self.Labelnumero1.pack()
        
        self.entrynumero1 = tk.Entry(ventana) 
        self.entrynumero1.pack()   
        
        self.Labelnumero2 = tk.Label(ventana, text='Dividendo:')
        self.Labelnumero2.pack()
        self.entrynumero2 = tk.Entry(ventana)
        self.entrynumero2.pack()
        
        self.boton = tk.Button(ventana, text='Dividir',command=self.dividir, **disenoBoton)
        self.boton.pack()

    def dividir(self):
        numero1 = int(self.entrynumero1.get())
        numero2 = int(self.entrynumero2.get())
        calculadora = Calculadora(numero1, numero2)
        resultado = calculadora.division()
        messagebox.showinfo(message="Resultado: "+str(resultado), title="Resultado")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()