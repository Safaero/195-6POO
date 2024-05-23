from tkinter import Tk, Label, Entry, Button
from indexerrormes2 import Mes

def mostrar_nombre():
    numero = int(entry.get())
    nombre_mes = mes.obtener_nombre(numero)
    label_resultado.config(text=nombre_mes)

#ventana
ventana = Tk()
ventana.title("Obtener nombre de mes")
ventana.geometry("300x300")


# Widget
length_label = Label(ventana, text="Ingrese el número del mes:")
length_label.place(x=50, y=30, width=200, height=30)

entry = Entry(ventana)
entry.place(x=50, y=70, width=200, height=30)

mes = Mes()

button = Button(ventana, text="Obtener nombre", command=mostrar_nombre, bg='#0D5CCE', fg='#FFFFFF')
button.place(x=50, y=110, width=200, height=30)

label_resultado = Label(ventana, text="")
label_resultado.place(x=50, y=150, width=200, height=30)

ventana.mainloop()
