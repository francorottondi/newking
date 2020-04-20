from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3








#class ProgramaNewKing:


wind=Tk()
wind.title("New King")
db_nk = 'database.db'
wind.iconbitmap("nk2.ico")




#-----------(funciones)---------

#---(Funciones Menú)----------
def acercadeMenu():
    messagebox.showinfo("Acerca de..","Prueba de Franco Rottondi\n para New King ")
def destruirRoot():
    decision=messagebox.askokcancel("Salir","¿Esta seguro que desa salir?")
    if decision:
        exit()
    else:
        pass


#------(Funciones app)------------

def run_query(query, parameters=()):
    with sqlite3.connect(db_nk) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

def get_products():
    global result
    #Limpiar tabla
    record=tree.get_children()
    for elementos in record:
        tree.delete(elementos)
    #consultando datos
    query = 'SELECT * FROM products ORDER BY name DESC'
    db_rows=run_query(query)
    for fila in db_rows:
        tree.insert('',index=0,text=fila[1],values=[fila[2],fila[3]])

def validacion():
    return len(name.get()) !=0 and len(price.get()) !=0 and len(rubro.get()) !=0


def agregar_producto():
    if validacion():
        query='INSERT INTO products VALUES(NULL,?,?,?)'
        parameters=(name.get(),price.get(),rubro.get())
        run_query(query,parameters)
        mensaje.config(text=f"Articulo {name.get()} ingresado satisfactoriamente", )
        name.delete(0,END)
        price.delete(0,END)
        rubro.delete(0,END)
    else:
        mensaje.config(text="Faltan datos a ingresar")
    get_products()

def delete_product():
    mensaje.config(text='')
    try:
        tree.item(tree.selection())['text'][0]
    except:
        messagebox.showwarning("Atencion","Selecciona lo que deseas eliminar")
        return
    name=tree.item(tree.selection())['text']
    seguro = messagebox.askyesno("Eliminar Articulo", f"Está seguro que desea eliminar {name}")
    if seguro:
        query='DELETE FROM products WHERE name = ?'
        run_query(query,(name, ))
        mensaje.config(text=f"El articulo {name} se elimino correctamente")
        get_products()
    else:
        pass



def edit_products():
    mensaje.config(text='')
    try:
        tree.item(tree.selection())['text'][0]
    except:
        messagebox.showwarning("Atencion", "Selecciona lo que deseas editar")
        return
    name = tree.item(tree.selection())['text']
    precio_viejo=tree.item(tree.selection())['values'][0]
    rubro_viejo=tree.item(tree.selection())['values'][1]

    #Ventana edicion
    ventanaedicion=Toplevel()
    ventanaedicion.title("Editar producto")
    ventanaedicion.iconbitmap("nk2.ico")


    #Nombre viejo
    Label(ventanaedicion, text='Antiguo Nombre: ').grid(row=0, column=1)
    Entry(ventanaedicion, textvariable=StringVar(ventanaedicion, value=name), state='readonly').grid(row=0, column=2)
    # Nuevo Nombre
    Label(ventanaedicion, text='Nuevo Nombre: ').grid(row=1, column=1)
    nombre_nuevo = Entry(ventanaedicion)
    nombre_nuevo.grid(row=1, column=2)
    nombre_nuevo.focus()
    # Precio antiguo
    Label(ventanaedicion, text='Precio Antiguo: ').grid(row=2, column=1)
    Entry(ventanaedicion, textvariable=StringVar(ventanaedicion, value=precio_viejo), state='readonly').grid(row=2,column=2)
    # Precio Nuevo
    Label(ventanaedicion, text='Precio Nuevo: ').grid(row=3, column=1)
    precio_nuevo = Entry(ventanaedicion)
    precio_nuevo.grid(row=3, column=2)
    # Rubro viejo
    Label(ventanaedicion, text='Antiguo Rubro: ').grid(row=4, column=1)
    Entry(ventanaedicion, textvariable=StringVar(ventanaedicion, value=rubro_viejo), state='readonly').grid(row=4, column=2)
    # Rubro Nombre
    Label(ventanaedicion, text='Nuevo Rubro: ').grid(row=5, column=1)
    rubro_nuevo = Entry(ventanaedicion)
    rubro_nuevo.grid(row=5, column=2)

    # Boton para aceptar cambios
    Button(ventanaedicion, text="Guardar Cambios",command=lambda: guardar_cambios(nombre_nuevo.get(), name, precio_nuevo.get(), precio_viejo,rubro_nuevo.get(),rubro_viejo)).grid(row=6, column=2,sticky=W)

    def guardar_cambios(nombre_nuevo,name,precio_nuevo,precio_viejo,rubro_nuevo,rubro_viejo):
        query = 'UPDATE products SET name = ?, price = ?, rubro = ? WHERE name = ?  AND price = ? AND rubro = ?'
        parameters = (nombre_nuevo, precio_nuevo, rubro_nuevo, name,precio_viejo,rubro_viejo)
        run_query(query, parameters)
        get_products()
        mensaje.config(text=f'El articulo {name} fue actualizado correctamente a {nombre_nuevo}')
        print(nombre_nuevo,precio_nuevo,rubro_nuevo)
        ventanaedicion.destroy()


#-----------(GUI)---------

#-----------(menu bar)---------

menubar = Menu(wind)
wind.config(menu=menubar)

ArchivoMenu=Menu(menubar,tearoff=0)
ayudaMenu=Menu(menubar,tearoff=0)

menubar.add_cascade(label="Archivo",menu=ArchivoMenu)
menubar.add_cascade(label="Ayuda",menu=ayudaMenu)

ayudaMenu.add_command(label="Acerca de...",command=acercadeMenu)
ArchivoMenu.add_command(label="Salir",command=destruirRoot)



# Creando # Frame Container (Recuadro que adentro permite tener elementos
frame = LabelFrame(wind, text='Registra un nuevo Producto')
frame.grid(row=0, column=0, columnspan=3, pady=20)

# Name input
Label(frame, text='Nombre: ').grid(row=1, column=0)
name = Entry(frame)
name.focus()
name.grid(row=1, column=1)

# Precio input
Label(frame, text='Precio: ').grid(row=2, column=0)
price = Entry(frame)
price.grid(row=2, column=1)

# Rubro input
Label(frame, text='Rubro: ').grid(row=3, column=0)
rubro = Entry(frame)
rubro.focus()
rubro.grid(row=3, column=1)

# Boton agregar producto
botproducto=Button(frame, text='Guardar Producto', command=agregar_producto)
botproducto.grid(row=4, columnspan=2, sticky=W + E)

# Mensaje al apretar boton
mensaje = Label(text='', fg='red')
mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

# Tabla
tree = ttk.Treeview(height=10,columns=('#0','#1'))
tree.grid(row=6, column=0, columnspan=2,sticky=W+E)
tree.heading('#0', text='Nombre', anchor=CENTER)
tree.heading('#1', text='Precio', anchor=CENTER)
tree.heading('#2', text='Rubro', anchor=CENTER)

vsb = Scrollbar(wind, orient="vertical", command=tree.yview)
vsb.place(relx=0.978, rely=0.445, relheight=0.490, relwidth=0.020)
tree.configure(yscrollcommand=vsb.set)


get_products()


# Boton Borrar/Editar/actualizar
botborr=Button(text='Borrar', command=delete_product)
botborr.grid(row=10, column=0, sticky=W + E)
botedit=Button(text='Editar', command=edit_products)
botedit.grid(row=10, column=1, sticky=W + E)











wind.mainloop()


#newking=ProgramaNewKing()
