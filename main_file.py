'''
Archivo ppal con paginas y botones
'''
import tkinter as tk
from tkinter import *
from functions_file import baseDeDatos,archivoTXT,imprimirGrafica,borrarTodo,volver

ventana = tk.Tk()
ventana.geometry('570x250')
#imagen


def paginaPpal():
    # tagOpcion= tk.Label(ventana, text="Opciones:", width=20, height=4, font="calibri",bg="cyan")
    # tagOpcion.place(x=10, y=120, width=80,height=30)
    botonManipulacion = tk.Button(ventana, text="Manipulacion de datos", command=pagina2)
    botonManipulacion.place(x=10, y=60,width=200,height=30)
    botonImprimir = tk.Button(ventana, text="Imprimir grafica de la base de datos",command=lambda: imprimirGrafica(ventana))
    botonImprimir.place(x=10, y=100,width=200, height=30)
    botonImprimir = tk.Button(ventana, text="Imprimir grafica de txt")
    botonImprimir.place(x=10, y=140,width=200, height=30)
    botonImprimir = tk.Button(ventana, text="Imprimir grafica de csv")
    botonImprimir.place(x=10, y=180,width=200, height=30)
    
    # labelAzul=tk.Label(ventana,bg='blueviolet')
    # labelAzul.place(x=220,y=0,relwidth=1,relheight=1)
    

def pagina2():
    # borro los widgets (botones y etiquetas(tags)) de la pagina1
    borrarTodo(ventana)   
    ventana.geometry("220x250") 
    '''
    botones de la pagina 2
    Boton para trabajar con la bd
    Llamo a la funcion baseDeDatos y le paso como argumento la ventana
    es necesario utilizar una funcion anonima para que la funcion se ejecute cuando hago 
    clic en el boton sin ejecutarse inmediatamente al definir el boton y arroje un 
    error:"can't invoke "button" command: application has been destroyed"
    '''    
    botonBD = tk.Button(ventana, text="Base de Datos", command=lambda: baseDeDatos(ventana,paginaPpal))
    botonBD.place(x=10, y=30, width=200,height=30)
    # Boton para trabajar con el archivo .csv
    botonCSV = tk.Button(ventana, text="CSV")
    botonCSV.place(x=10, y=70, width=200,height=30)
    # Boton para trabajar con el archivo .txt
    botonTXT = tk.Button(ventana, text="txt", command=lambda: archivoTXT(ventana,paginaPpal))
    botonTXT.place(x=10, y=110, width=200,height=30)
    # boton para volver a la pagina ppal
    botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
    botonVolver.place(x=10, y=190, width=200,height=30)
    
    
    # labelAzul=tk.Label(ventana,bg='blueviolet')
    # labelAzul.place(x=220,y=0,relwidth=1,relheight=1)



#programa conductor
#pagina ppal o pagina1
ventana.config(bg="cyan")
    # Creo imagen y la redimensiono para que conserve la proporción
imga = PhotoImage(file="ventas.gif")
imga = imga.subsample(int(imga.width() / 300))  # Ajusto el ancho
imga = imga.zoom(int(imga.width() / 300))  # Ajusto el alto

lblImage = Label(ventana, image=imga)
lblImage.place(x=220, y=10)  # Empaqueto el Label con la imagen



ventana.title("Sistema de gestion de Ventas")
paginaPpal() # funcion con botones de la pagina ppal 

ventana.mainloop()