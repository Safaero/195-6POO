from tkinter import Tk, Frame, Button, messagebox, Label, Entry, ttk, Checkbutton, BooleanVar
from Controller import *
controlador = Controller()

def verificarEdad():
    edad = int(txtEdad.get())
    validacion = 0
    
    try:
        validacion = controlador.verificarEdadCont(edad)
    except ExcepcionEdadInvalida as e:
        print("Error", e)
    
    if validacion == 1:
        lblVerif.config(text="Eres Mayor de edad",bg="green")
    else:
        lblVerif.config(text="Eres Menor de edad",bg="red")
    

def buscarUsuario():
    nombre = txtNombre.get()
    busqueda = 0
    
    try:
        busqueda = controlador.buscarNombre(nombre)
    except ExcepcionNombre as e:
        print("Error", e)
    
    if busqueda == 1:
        lblBusq.config(text="Usuario Encontrado",bg="green")
    else:
        lblBusq.config(text="Usuario no encontrado",bg="red")


frame = Tk() 
frame.title('Excepciones Personalizadas')
frame.geometry('500x500')

fondo = Frame(frame,bg="white")
fondo.pack(expand=True,fill="both")

#-- 

lblEdad = Label(fondo,text='Escribe tu edad',bg='white')
lblEdad.place(x='10',y='60')

txtEdad = Entry(fondo)
txtEdad.configure(width='30')
txtEdad.place(x='10',y='100')

btnVerificar= Button(fondo,text="Verificar edad",bg='lightgray',command= verificarEdad)
btnVerificar.configure(width='15',height='1')
btnVerificar.place(x='10',y='130')

lblVerif = Label(fondo,text='',bg='white')
lblVerif.place(x='10',y='170')

#-- 

lblNombre = Label(fondo,text='Escribe tu nombre',bg='white')
lblNombre.place(x='10',y='220')

txtNombre = Entry(fondo)
txtNombre.configure(width='30')
txtNombre.place(x='10',y='250')

btnBuscar= Button(fondo,text="Buscar Nombre",bg='lightgray',command= buscarUsuario)
btnBuscar.configure(width='15',height='1')
btnBuscar.place(x='10',y='280')

lblBusq = Label(fondo,text='',bg='white')
lblBusq.place(x='10',y='330')



frame.mainloop()