'''Archivo con funciones de tipo csv, txt y bd; y botones'''
#pagina 3 o bd
import mysql.connector
from mysql.connector import Error
import tkinter as tk 
from tkinter import ttk

def create_gradient_background(canvas, colors, width, height):
    num_colors = len(colors)
    color_height = height // (num_colors - 1)
    
    for i in range(num_colors - 1):
        color1 = colors[i]
        color2 = colors[i + 1]
        for j in range(color_height):
            r = int(color1[0] * (1 - j / color_height) + color2[0] * (j / color_height))
            g = int(color1[1] * (1 - j / color_height) + color2[1] * (j / color_height))
            b = int(color1[2] * (1 - j / color_height) + color2[2] * (j / color_height))
            canvas.create_rectangle(0, (i * color_height) + j, width, (i * color_height) + j + 1, fill='#%02x%02x%02x' % (r, g, b), outline='')

def funcionesdegradado(ventana):
    canvas = tk.Canvas(ventana, width=550, height=300)
    canvas.place(x=240,y=0)
    colors = [(0, 0, 75), (138, 43, 226), (0, 0, 75)]
    return canvas, colors


def volver(ventana,paginaPpal):
    borrarTodo(ventana)
    paginaPpal()

def borrarTodo(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
        
def baseDeDatos(ventana,paginaPpal): # acepto la ventana como parametro
    # base de datos   
    # borrar elementos que habia en la pagina1
    borrarTodo(ventana)
    
    def conectarse_bd(usuario,contrasenia):
        # conectarse a la base de datos
        conexion = None
        try: 
            conexion= mysql.connector.connect(
                host="localhost",
                user=usuario,
                password=contrasenia,
                database= 'ventas'
            )
            if conexion: 
                print("conexion realizada correctamente")
                return conexion # retorno la conexion
            
        except Error as e:
            print("ha ocurrido un error:")
            print(e)
    
    
    def obtener_datos(conexion):# recibe el contenido de la tabla de la base de datos
        cursor= conexion.cursor()
        cursor.execute("SELECT * FROM tabladventas")
        #obtener todos los resultados
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    # funcion para agregar un producto que fue vendido            
    def agregar(conexion):
        def agregarProductoAlaBD(conexion):
            nombre = nombreProducto.get()
            precio = precioProducto.get()
            if nombre and precio:
                # conexion = conectarse_bd            
                cursor = conexion.cursor()   #creo un objeto cursor     
                query = "INSERT INTO tabladventas (nombre, precio) VALUES (%s, %s)"
                values = (nombre, precio)
                cursor.execute(query, values)
                conexion.commit()
                cursor.close()
                conexion.close()
                # mensaje para avisar que se agrego el dato en la bd con foreground verde
                mensaje.config(text="Producto agregado correctamente.", fg="green")
            else:
                # mensaje de error
                mensaje.config(text="Por favor, ingrese un nombre y un precio.", fg="red")
        # flujo de la ventana de para agregar venta a la bd
        borrarTodo(ventana)
        #etiquetas y campos de entrada
        tagNombre = tk.Label(ventana, text="Nombre del producto:")
        nombreProducto = tk.Entry(ventana)
        
        tagPrecio = tk.Label(ventana, text="Precio del producto:")
        precioProducto = tk.Entry(ventana)
        
        tagNombre.pack()        
        nombreProducto.pack()
        tagPrecio.pack()
        precioProducto.pack()
                
        #Boton para agregar el producto en la bd
        boton_agregar = tk.Button(ventana, text="Agregar producto", command=lambda: agregarProductoAlaBD(conexion))
        boton_agregar.pack()
        # etiqueta para mostrar mensajes
        mensaje = tk.Label(ventana, text='', fg="black")
        mensaje.pack()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()

    def modificar_entradasytags(conexion):
        borrarTodo(ventana)
        label_id= tk.Label(ventana, text="ID:")
        label_id.pack()
        entry_id = tk.Entry(ventana)
        entry_id.pack()
        
        label_nombre = tk.Label(ventana,text="Nombre: ")
        label_nombre.pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()
        
        label_precio = tk.Label(ventana,text="Precio: ")
        label_precio.pack()
        entry_precio = tk.Entry(ventana)
        entry_precio.pack()
        
        boton_modificar = tk.Button(ventana, text="Modificar",command=lambda: modificar(conexion, entry_id, entry_nombre, entry_precio))
        boton_modificar.pack()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
        
    def modificar(conexion, entry_id, entry_nombre, entry_precio):
        
        id_value = entry_id.get()
        nombre_value = entry_nombre.get()
        precio_value = entry_precio.get()
        id_value=int(id_value)
        #variable sql
        sql = "UPDATE tabladventas SET nombre = %s, precio = %s WHERE id = %s"
        print(sql)
        values = (nombre_value, precio_value, id_value)
        #creo un cursor para ejecutar consultas sql
        cursor= conexion.cursor()
        #ejecutar la declaracion de actualizacion
        cursor.execute(sql, values)
        #confirmar los cambios en la base de datos
        conexion.commit()
        # imprimir mensaje de exito
        print("Datos actualizados correctamente")
        
        
    def desconectarse(conexion):
        #cerrar la conexion al servidor mysql
        if conexion:
            conexion.close()
            print('conexion cerrada correctamente')
    # funcion para mostrar en una tabla los datos de la bd
    def mostrar_tabla(datos):
        borrarTodo(ventana)
        # crea una tabla (Treeview) en la ventana para mostrar los datos de la tabla de la bd
        tabla = ttk.Treeview(ventana, columns=("columna1", "columna2", "columna3"))
        # Encabezado de las columnas
        tabla.heading('columna1', text='ID')
        tabla.heading('columna2', text='Nombre del producto')
        tabla.heading('columna3', text='Precio')
        #obtener los datos de la base de datos
        # Ajustar el ancho de las columnas
        tabla.column('columna1', width=50)
        tabla.column('columna2', width=100)
        tabla.column('columna3', width=50)
        # lleno la tabla con los datos
        for fila in datos:
            tabla.insert('', 'end', values=fila)
        
        # mostrar tabla en la ventana
        tabla.pack()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
        ventana.mainloop()        
        desconectarse(conexion)
        
    
    
    def eliminarProducto(conexion):
        def eliminar():
            cursor= conexion.cursor()
            print('===============================')
            nombre_value= entry_nombre.get()
            print(nombre_value)
            print(type(nombre_value))
            sql = "DELETE FROM tabladventas WHERE nombre = %s"
            #le paso a la variable sql el nombre a eliminar con su info
            cursor.execute(sql, (nombre_value,)) #parentecis porque se string
            conexion.commit()
            cursor.close()
            print("exito")
        # borro witgets (botones de la pagina anterior)
        borrarTodo(ventana)
        #etiqueta y entrada
        label_nombre = tk.Label(ventana,text="Nombre: ")
        label_nombre.pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()
        # tomo el nombre que escribio en la entrada
        nombre_value= entry_nombre.get()
        # boton para confirmar el nombre a borrar
        botonDelete= tk.Button(ventana,text="Eliminar producto",command= eliminar)
        botonDelete.pack()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
    
    
    #flujo principal de trabajo con la bd
    usuario="root"
    contrasenia=""
    conexion=conectarse_bd(usuario,contrasenia)
    # botones
    botonMostrar = tk.Button(ventana, text="Mostrar",command= lambda: mostrar_tabla(obtener_datos(conexion)))
    botonMostrar.place(x=10, y=30,width=200,height=30)
    botonAgregar = tk.Button(ventana, text="Agregar producto",command= lambda: agregar(conexion))
    botonAgregar.place(x=10, y=70,width=200,height=30)
    botonModificar = tk.Button(ventana, text="Modificar", command=lambda: modificar_entradasytags(conexion))
    botonModificar.place(x=10, y=110,width=200,height=30)
    #boton que abre borra lo que hay en la ventana y pone una entrada para ingresar el nombre a eliminar
    botonEliminar = tk.Button(ventana, text="Eliminar producto de la base", command=lambda: eliminarProducto(conexion))
    botonEliminar.place(x=10, y=150,width=200,height=30)
    # boton para volver a la pagina ppal
    botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
    botonVolver.place(x=10, y=190,width=200,height=30)

    
# txt
def archivoTXT(ventana,paginaPpal):
    borrarTodo(ventana)
    #Función para agregar datos en formato txt
    def agregar_txt(ventana): 
        def agrega(nombreProductot, precioProductot):
            
            name = nombreProductot.get() #asigno el valor que esta en el entry nombreProductot a name
            price = precioProductot.get()     
            if price.isdigit(): 
                producto = name + ' ' + price + '\n'
                with open('ventas.txt', 'a') as archivo:
                    archivo.write(producto)
            else:
                print('Ingreso caracteres incorrectos')             

        def entradasybotones():
            borrarTodo(ventana)

            tagNombre = tk.Label(ventana, text="Nombre del producto:")
            tagNombre.pack()
            nombreProductot = tk.Entry(ventana)
            nombreProductot.pack()

            tagPrecio = tk.Label(ventana, text="Precio del producto:")
            tagPrecio.pack()
            precioProductot = tk.Entry(ventana)
            precioProductot.pack()

            botonAgregarP = tk.Button(ventana, text='Agregar', command=lambda: agrega(nombreProductot, precioProductot))
            botonAgregarP.pack()

            
        #flujo para agregar, llamo al procedimiento
        entradasybotones()
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
        
        

    
        
    # Función para mostrar los datos en formato txt
    def mostrar_txt(ventana):
        def leer_archivo():
            datos = [] #lista para almacenar los datos leido y separados por espacios para dividir la linea
            try: 
                with open("ventas.txt",'r') as archivo:
                    lineas = archivo.readlines()
                    #creo una lista de cada linea y la agrego a la lista 'datos'
                    for linea in lineas:
                        datos.append(linea.split()) # split separa por defecto por espacio
            except FileNotFoundError:
                print("El archivo no se encuentra o no se puede leer.")

            return datos
    
        def mostrar_tabla(datos):
            tabla = ttk.Treeview(ventana)
            tabla['columns'] = ('Precio')
            tabla.column('#0', width=100, minwidth=100)
            tabla.column('Precio', anchor=tk.W, width=100)
            tabla.heading('#0', text='Nombre')
            tabla.heading('Precio', text='Precio')

            for i, (nombre, precio) in enumerate(datos):
                tabla.insert(parent='', index='end', iid=i, text=nombre, values=(precio,))

            tabla.pack()
        #flujo de mostrar tabla
        borrarTodo(ventana)
        datos = leer_archivo()
        mostrar_tabla(datos) #envio los datos en una lista con listas (cada sublista tiene como elemento nombre y precio)
        # boton para volver a la pagina ppal
        botonVolver = tk.Button(ventana,text="volver atras",command=lambda: volver(ventana,paginaPpal))
        botonVolver.pack()
            
    def modificar_txt(ventana):        
        def modificart(entry_nombret, entry_preciot, entry_nombren, entry_precion):
            nombre_value = entry_nombret.get()
            precio_value = entry_preciot.get()
            nombre_nuevo = entry_nombren.get()
            precio_nuevo = entry_precion.get()
            lineaAmodificar = nombre_value + ' ' + precio_value + '\n'
            nuevo = nombre_nuevo + ' ' + precio_nuevo + '\n'

            with open('ventas.txt', 'r') as archivo:
                lineas = archivo.readlines()

            lista = []
            for linea in lineas:
                if linea == lineaAmodificar:
                    lista.append(nuevo)
                else:
                    lista.append(linea)

            with open('ventas.txt', 'w') as archivo:
                archivo.writelines(lista)

            print("Datos actualizados correctamente")

        def modificar_txt_entradasytags():
            borrarTodo(ventana)
            
            label_nombret = tk.Label(ventana, text="Nombre del producto a modificar: ")
            label_nombret.pack()
            entry_nombret = tk.Entry(ventana)
            entry_nombret.pack()

            label_preciot = tk.Label(ventana, text="Precio del producto a modificar: ")
            label_preciot.pack()
            entry_preciot = tk.Entry(ventana)
            entry_preciot.pack()
            
            # nombre y precio nuevo
            label_nombren = tk.Label(ventana, text="Nuevo nombre: ")
            label_nombren.pack()
            entry_nombren = tk.Entry(ventana)
            entry_nombren.pack()
            
            label_precion = tk.Label(ventana, text="Nuevo precio: ")
            label_precion.pack()
            entry_precion = tk.Entry(ventana)
            entry_precion.pack()
            
            boton_modificart = tk.Button(ventana, text="Modificar", command=lambda: modificart(entry_nombret, entry_preciot, entry_nombren, entry_precion))
            boton_modificart.pack()
            
            botonVolver = tk.Button(ventana, text="Volver atras", command=lambda: volver(ventana, paginaPpal))
            botonVolver.pack()

        modificar_txt_entradasytags()

        
    def eliminar_txt(ventana):
        def eliminart(entry_nombre, entry_precio):
            nombre_value = entry_nombre.get()
            precio_value = entry_precio.get()
            lineaAeliminar = nombre_value + ' ' + precio_value + '\n'

            with open('ventas.txt', 'r') as archivo:
                lineas = archivo.readlines()

            with open('ventas.txt', 'w') as archivo:
                for linea in lineas:
                    if linea != lineaAeliminar:
                        archivo.write(linea)

        def eliminar_en_txt_entradasytags():
            borrarTodo(ventana)

            label_nombret = tk.Label(ventana, text="Nombre a eliminar: ",bg="cyan")
            label_nombret.place(x=10, y=20,width=200,height=20)
            entry_nombret = tk.Entry(ventana)
            entry_nombret.place(x=10, y=50,width=200,height=20)

            label_preciot = tk.Label(ventana, text="Precio del nombre a eliminar: ",bg="cyan")
            label_preciot.place(x=10, y=80,width=200,height=20)
            entry_preciot = tk.Entry(ventana)
            entry_preciot.place(x=10, y=110,width=200,height=20)

            boton_eliminart = tk.Button(ventana, text="Eliminar", command=lambda: eliminart(entry_nombret, entry_preciot))
            boton_eliminart.place(x=10, y=140,width=200,height=25)

            botonVolver = tk.Button(ventana, text="Volver atras", command=lambda: volver(ventana, paginaPpal))
            botonVolver.place(x=10, y=195,width=200,height=25)

        eliminar_en_txt_entradasytags()

    
    
    #flujo del pagina txt
    # botones
    botonMostrar = tk.Button(ventana, text="Mostrar",command= lambda: mostrar_txt(ventana))
    botonMostrar.place(x=10, y=30,width=200,height=30)
    botonAgregar = tk.Button(ventana, text="Agregar producto",command= lambda: agregar_txt(ventana))
    botonAgregar.place(x=10, y=70,width=200,height=30)
    botonModificar = tk.Button(ventana, text="Modificar", command=lambda: modificar_txt(ventana))
    botonModificar.place(x=10, y=110,width=200,height=30)
    #boton que abre borra lo que hay en la ventana y pone una entrada para ingresar el nombre a eliminar
    botonEliminar = tk.Button(ventana, text="Eliminar producto", command=lambda: eliminar_txt(ventana))
    botonEliminar.place(x=10, y=150,width=200,height=30)


def archivoCSV(ventana):
    borrarTodo(ventana)

    def cargar_datos_csv():
        try:
            df = pd.read_csv('ventas.csv')
            return df
        except FileNotFoundError:
            print("El archivo CSV no existe.")
            return pd.DataFrame()

    
    
    pass                
    





#imprimir grafico de barras con matplotlib
    
def imprimirGrafica(ventana):
    #sql
    import matplotlib.pyplot as plt

    def obtener_datos_vendidos():
        try:
            # Conectarse a la base de datos
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ventas"
            )

            if conexion.is_connected():
                cursor = conexion.cursor()

                # Consulta SQL para obtener la cantidad de ventas por producto
                query = "SELECT nombre, COUNT(*) AS cantidad FROM tabladventas GROUP BY nombre"
                cursor.execute(query)

                resultados = cursor.fetchall()

                return resultados

        except Error as e:
            print("Error al conectar a la base de datos:", e)
            return []

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def crear_grafico_de_barras():
        datos = obtener_datos_vendidos()

        if not datos:
            print("No se encontraron datos para crear el gráfico.")
            return #para salir?

        nombres_productos, cantidad_ventas = zip(*datos)

        plt.bar(nombres_productos, cantidad_ventas)
        plt.xlabel("Productos")
        plt.ylabel("Cantidad de Ventas")
        plt.title("Cantidad de Ventas por Producto")

        # Guardar el gráfico en un archivo de imagen en formato JPG        
        # plt.savefig("image.jpg")
        # muestro el grafico de barras con la cantidad de ventas por producto
        plt.show()
        
    # Llamar a la función para crear el gráfico
    imagen = crear_grafico_de_barras()

    

    #csv
    
    #txt
    
    
