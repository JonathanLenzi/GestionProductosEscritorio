from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

import tk as tk


def salirDelPrograma():  # funcion para salir del programa

    valor = messagebox.askquestion("Salir", "¿Realmente quiere salir del programa?")

    if valor == "yes":
        root.destroy()  # cierra el programa




class Producto():
    db="database/productos.db"
    def __init__(self, root):
        self.ventana= root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1)#redimencionable
        self.ventana.wm_iconbitmap("recursos/logocuart.ico")


        # creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana,
                           text="Registrar un nuevo Producto")  # hay que pasarle donde queremos que se ejecute
        # posicionar frame, columnspan=cantidad de columnas,pady=margen
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre= Label(frame, text="Nombre: ")
        #posicionar
        self.etiqueta_nombre.grid(row=1,column=0)
        #entry nombre
        self.nombre= Entry(frame)
        self.nombre.focus()
        #posicion
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        # posicionar
        self.etiqueta_precio.grid(row=2, column=0)
        # entry precio
        self.precio = Entry(frame)
        # posicion
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ")
        # posicionar
        self.etiqueta_categoria.grid(row=3, column=0)
        # entry categoria
        self.categoria = Entry(frame)
        # posicion
        self.categoria.grid(row=3, column=1)

        # Label stock
        self.etiqueta_stock = Label(frame, text='Stock: ')
        self.etiqueta_stock.grid(row=2, column=2)
        # Entry stock
        self.stock = Entry(frame)
        self.stock.grid(row=2, column=3)

        #Boton de añadir producto                                  #en command el metodo add sin parentesis!!
        self.boton_aniadir= ttk.Button(frame,text = "Guardar Producto", command= self.add_producto)
        self.boton_aniadir.grid(row=4, columnspan= 2, sticky= W + E)


        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='green')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W + E)



        #Tabla Productos
        style = ttk.Style()
        # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11))
        # Se modifica la fuente de las cabeceras
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        # Eliminamos los bordes
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])

        # TABLA DE PRODCUTOS (Treeview)
        # Estilo propio
        s = ttk.Style()
        s.configure('my.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))  # fuente de la tabla
        s.configure('my.Treeview.Heading', font=('Calibri', 13, 'bold'))  # fuente de las cabeceras
        s.layout('my.Treeview', [('my.Treeview.treearea', {'sticky': 'nswe'})])  # eliminase los bordes
        # Estrutura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#0', '#1', '#2'), style='my.Treeview')
        self.tabla.grid(row=5, column=0, columnspan=4)
        self.tabla.heading('#0', text='NOMBRE ⚀', anchor='center')
        self.tabla.heading('#1', text='PRECIO ⚁', anchor='center')
        self.tabla.heading('#2', text='CATEG  ⚂', anchor='center')
        self.tabla.heading('#3', text='CANT ⚃', anchor='center')
        self.tabla.column('#1', anchor='center')
        self.tabla.column('#3', anchor='center')

        #Boton de Eliminar y Editar
        s=ttk.Style()
        s.configure("my.TButton", font=("calibri", 14, "bold"))
        boton_eliminar=ttk.Button(text= "ELIMINAR", style="my.TButton",command= self.del_producto)
        boton_eliminar.grid(row=6, column=0, sticky=W+E)
        boton_editar=ttk.Button(text="EDITAR", style="my.TButton",command=self.edit_producto)
        boton_editar.grid(row=6, column=1, sticky=W + E)
        #Barra de despazamiento
        barra = Scrollbar(self.ventana, orient='vertical', command=self.tabla.yview)
        barra.grid(column=4, row=5, sticky='ns')
        self.tabla.configure(yscrollcommand=barra.set)
        #actualizamos tabla
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):#recibe consulta
        with sqlite3.connect(self.db) as con: #establecer connexion con la base de datos
            cursor=con.cursor()
            resultado=cursor.execute(consulta,parametros)#obenemos resultado
            con.commit()
        return resultado #devuelve

    def get_productos(self):

        registros_tabla= self.tabla.get_children()
        for fila in registros_tabla:#primero la elimino
            self.tabla.delete(fila)

        query= "SELECT * FROM producto ORDER BY nombre DESC"
        registros_db= self.db_consulta(query)

        for fila in registros_db:  #luego la creo nuevamente
            print(fila)
            self.tabla.insert("", 0, text= fila[1], values=(fila[2],fila[3],fila[4]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0
    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query= "INSERT INTO producto VALUES(NULL,?,?,?,?)"
            parametros=(self.nombre.get(),self.precio.get(),self.categoria.get(),self.stock.get())#tiene que ser una tupla
            self.db_consulta(query,parametros)
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
            self.stock.delete(0, END)  # Borrar el campo stock del formulario
        elif (not self.validacion_nombre() or not self.validacion_precio() or not self.validacion_categoria()
              or not self.validacion_stock() ):
            self.mensaje['text'] = ('TODOS LOS CAMPOS SON OBLIGATORIOS')

        self.get_productos()#volvemos a actualizar la lista

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        categoria = self.tabla.item(self.tabla.selection())['values'][
            1]  # La categoria se encuentra dentro de una lista
        stock = self.tabla.item(self.tabla.selection())['values'][2]  # El stock se encuentra dentro de una lista

        # Ventana nueva(editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/logocuart.ico')  # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto",
                              font=('Calibri', 16, 'bold'))  # frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ",
                                              font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly', font=('Calibri', 13, 'bold'))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ",
                                              font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        # Entry Precio antiguo(texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=('Calibri', 13, 'bold'))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antiugua = Label(frame_ep, text="Categoria antigua: ",
                                                 font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_antiugua.grid(row=6, column=0)  # Posicionamiento a traves de grid

        # Entry Categoria antigua(texto que no se podra modificar)
        self.input_categoria_antiugua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria),
                                              state='readonly', font=('Calibri', 13, 'bold'))
        self.input_categoria_antiugua.grid(row=6, column=1)

        # Label Categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)

        # Entry Categoria nuevo (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_anituguo = Label(frame_ep, text="Stock antiguo: ",
                                             font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_anituguo.grid(row=8, column=0)  # Posicionamiento a traves de grid

        # Entry Stock antiguo(texto que no se podra modificar)
        self.input_stock_anituguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=stock),
                                          state='readonly', font=('Calibri', 13, 'bold'))
        self.input_stock_anituguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)

        # Entry Stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),
                                  self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(),
                                  self.input_precio_antiguo.get(),
                                  self.input_categoria_nueva.get(),
                                  self.input_categoria_antiugua.get(),
                                  self.input_stock_nuevo.get(),
                                  self.input_stock_anituguo.get()))

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria,
                             antigua_categoria, nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':  # Si el usuario escribe nuevo nombre,nuevo precio,nueva categoria y nuevo stock se cambian
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (
                antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre y el precio, se mantiene el nombre y el precio anterior
            parametros = (
                antiguo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre, el precio y la categoria, se mantiene el nombre, el precio y la categoria anteriores
            parametros = (
                antiguo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre y la categoria, se mantiene el nombre y la categoria anterior
            parametros = (
                antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre, la categoria y el stock, se mantiene el nombre y la categoria y el stock anterior
            parametros = (
                antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre y el stock, se mantiene el nombre y el stock anterior
            parametros = (
                antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre, el precio y el stock, se mantiene el nombre, el precio y el stock anterior
            parametros = (
                antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (
                nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo precio y la categoria, se mantiene el precio y la categoria anterior
            parametros = (
                nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo precio, la categoria y el stock, se mantiene el precio, la categoria y el stock anterior
            parametros = (
                nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo precio y el stock, se mantiene el precio y el stock anterior
            parametros = (
                nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio la nueva categoria, se mantiene la categoria anterior
            parametros = (
                nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio la nueva categoria, se mantiene la categoria anterior
            parametros = (
                nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo stock, se mantiene el stock anterior
            parametros = (
                nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(
                antiguo_nombre)  # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(
                antiguo_nombre)  # Mostrar mensaje para el usuario


if __name__ == "__main__":
    root = Tk() # abrimos ventana grafica
    app = Producto(root)#creo objeto primero y le paso la ventana
    root.mainloop() #Con esto nuestra ventana queda abierta




