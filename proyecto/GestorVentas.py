import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# Conexion a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Giuseppe200410",
        database="gestion_ventas"
    )

# Funciones para gestion de productos
def agregar_producto():
    conn = conectar_bd()
    cursor = conn.cursor()
    nombre = entry_nombre_producto.get()
    categoria = entry_categoria.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    try:
        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, categoria, precio, stock)
        )
        conn.commit()
        messagebox.showinfo("Exito", "Producto agregado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def modificar_producto():
    conn = conectar_bd()
    cursor = conn.cursor()
    id_producto = entry_id_producto.get()
    nombre = entry_nombre_producto.get()
    categoria = entry_categoria.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    try:
        cursor.execute(
            "UPDATE productos SET nombre = %s, categoria = %s, precio = %s, stock = %s WHERE id_producto = %s",
            (nombre, categoria, precio, stock, id_producto)
        )
        conn.commit()
        messagebox.showinfo("Exito", "Producto modificado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def eliminar_producto():
    conn = conectar_bd()
    cursor = conn.cursor()
    id_producto = entry_id_producto.get()
    try:
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conn.commit()
        messagebox.showinfo("Exito", "Producto eliminado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def ver_productos():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        ver_productos_text.delete("1.0", tk.END)
        for producto in productos:
            ver_productos_text.insert(tk.END, f"ID: {producto[0]}, Nombre: {producto[1]}, Categoria: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

# Funciones para gestion de clientes
def agregar_cliente():
    conn = conectar_bd()
    cursor = conn.cursor()
    nombre = entry_nombre_cliente.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()
    try:
        cursor.execute(
            "INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s)",
            (nombre, correo, telefono)
        )
        conn.commit()
        messagebox.showinfo("Exito", "Cliente registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def modificar_cliente():
    conn = conectar_bd()
    cursor = conn.cursor()
    id_cliente = entry_id_cliente.get()
    nombre = entry_nombre_cliente.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()
    try:
        cursor.execute(
            "UPDATE clientes SET nombre = %s, correo = %s, telefono = %s WHERE id_cliente = %s",
            (nombre, correo, telefono, id_cliente)
        )
        conn.commit()
        messagebox.showinfo("Exito", "Cliente modificado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def eliminar_cliente():
    conn = conectar_bd()
    cursor = conn.cursor()
    id_cliente = entry_id_cliente.get()
    try:
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        messagebox.showinfo("Exito", "Cliente eliminado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def ver_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        ver_clientes_text.delete("1.0", tk.END)
        for cliente in clientes:
            ver_clientes_text.insert(tk.END, f"ID: {cliente[0]}, Nombre: {cliente[1]}, Correo: {cliente[2]}, Telefono: {cliente[3]}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()
        
def buscar_productos_avanzada():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    precio_min = entry_precio_min.get()
    precio_max = entry_precio_max.get()

    if precio_min and not precio_min.isdigit():
        messagebox.showerror("Error", "El precio minimo debe ser un numero valido.")
        return
    if precio_max and not precio_max.isdigit():
        messagebox.showerror("Error", "El precio maximo debe ser un numero valido.")
        return
    
    query = "SELECT * FROM productos WHERE 1=1"
    parametros = []
    
    if precio_min:
        query += " AND precio >= %s"
        parametros.append(precio_min)
    
    if precio_max:
        query += " AND precio <= %s"
        parametros.append(precio_max)
    
    try:
        cursor.execute(query, tuple(parametros))
        productos = cursor.fetchall()
        
        ver_productos_text.delete("1.0", tk.END)
        
        if productos:
            for producto in productos:
                ver_productos_text.insert(tk.END, f"ID: {producto[0]}, Nombre: {producto[1]}, Categoria: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}\n")
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron productos con esos filtros.")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


# Funciones para Ordenes
def mostrar_ordenes():
    conn = conectar_bd()
    cursor = conn.cursor()
    id_cliente = entry_id_cliente_orden.get()

    if not id_cliente:
        messagebox.showerror("Error", "Por favor ingrese un ID de cliente valido.")
        return

    try:
        cursor.execute(
            "SELECT ordenes.id_orden, productos.nombre, ordenes.fecha, ordenes.cantidad "
            "FROM ordenes "
            "JOIN productos ON ordenes.id_producto = productos.id_producto "
            "WHERE ordenes.id_cliente = %s",
            (id_cliente,)
        )
        
        ordenes = cursor.fetchall()
        
        if not ordenes:
            messagebox.showinfo("Sin Resultados", "No se encontraron ordenes para este cliente.")
            ordenes_text.delete("1.0", tk.END)
            return

        ordenes_text.delete("1.0", tk.END)
        
        for orden in ordenes:
            ordenes_text.insert(tk.END, f"ID Órden: {orden[0]}, Producto: {orden[1]}, Fecha: {orden[2]}, Cantidad: {orden[3]}\n")
    
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al obtener las ordenes: {str(e)}")
    finally:
        conn.close()

# Funciones de Reporte
def reporte_mas_vendido():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT productos.nombre, SUM(ordenes.cantidad) AS total "
            "FROM ordenes "
            "JOIN productos ON ordenes.id_producto = productos.id_producto "
            "GROUP BY productos.id_producto "
            "ORDER BY total DESC "
            "LIMIT 1"
        )
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showinfo("Producto Mas Vendido", f"Producto: {resultado[0]}, Total Vendido: {resultado[1]}")
        else:
            messagebox.showinfo("Producto Mas Vendido", "No se encontraron datos.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

# Interfaz Tkinter
root = tk.Tk()
root.title("Gestion de Ventas")
root.geometry("1000x700")

# Pestañas
tab_control = ttk.Notebook(root)

# Gestion de Productos
productos_tab = ttk.Frame(tab_control)
tab_control.add(productos_tab, text="Gestion de Productos")

ttk.Label(productos_tab, text="ID Producto:").grid(row=0, column=0, padx=10, pady=10)
entry_id_producto = ttk.Entry(productos_tab)
entry_id_producto.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(productos_tab, text="Nombre:").grid(row=1, column=0, padx=10, pady=10)
entry_nombre_producto = ttk.Entry(productos_tab)
entry_nombre_producto.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(productos_tab, text="Categoria:").grid(row=2, column=0, padx=10, pady=10)
entry_categoria = ttk.Entry(productos_tab)
entry_categoria.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(productos_tab, text="Precio:").grid(row=3, column=0, padx=10, pady=10)
entry_precio = ttk.Entry(productos_tab)
entry_precio.grid(row=3, column=1, padx=10, pady=10)

ttk.Label(productos_tab, text="Stock:").grid(row=4, column=0, padx=10, pady=10)
entry_stock = ttk.Entry(productos_tab)
entry_stock.grid(row=4, column=1, padx=10, pady=10)

btn_agregar = ttk.Button(productos_tab, text="Agregar Producto", command=agregar_producto)
btn_agregar.grid(row=5, column=0, padx=10, pady=10)

btn_modificar = ttk.Button(productos_tab, text="Modificar Producto", command=modificar_producto)
btn_modificar.grid(row=5, column=1, padx=10, pady=10)

btn_eliminar = ttk.Button(productos_tab, text="Eliminar Producto", command=eliminar_producto)
btn_eliminar.grid(row=6, column=0, padx=10, pady=10)

btn_ver_productos = ttk.Button(productos_tab, text="Ver Productos", command=ver_productos)
btn_ver_productos.grid(row=6, column=1, padx=10, pady=10)

ver_productos_text = tk.Text(productos_tab, height=10, width=60)
ver_productos_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Gestion de Clientes
clientes_tab = ttk.Frame(tab_control)
tab_control.add(clientes_tab, text="Gestion de Clientes")

ttk.Label(clientes_tab, text="ID Cliente:").grid(row=0, column=0, padx=10, pady=10)
entry_id_cliente = ttk.Entry(clientes_tab)
entry_id_cliente.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(clientes_tab, text="Nombre:").grid(row=1, column=0, padx=10, pady=10)
entry_nombre_cliente = ttk.Entry(clientes_tab)
entry_nombre_cliente.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(clientes_tab, text="Correo:").grid(row=2, column=0, padx=10, pady=10)
entry_correo = ttk.Entry(clientes_tab)
entry_correo.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(clientes_tab, text="Telefono:").grid(row=3, column=0, padx=10, pady=10)
entry_telefono = ttk.Entry(clientes_tab)
entry_telefono.grid(row=3, column=1, padx=10, pady=10)

btn_agregar_cliente = ttk.Button(clientes_tab, text="Agregar Cliente", command=agregar_cliente)
btn_agregar_cliente.grid(row=4, column=0, padx=10, pady=10)

btn_modificar_cliente = ttk.Button(clientes_tab, text="Modificar Cliente", command=modificar_cliente)
btn_modificar_cliente.grid(row=4, column=1, padx=10, pady=10)

btn_eliminar_cliente = ttk.Button(clientes_tab, text="Eliminar Cliente", command=eliminar_cliente)
btn_eliminar_cliente.grid(row=5, column=0, padx=10, pady=10)

btn_ver_clientes = ttk.Button(clientes_tab, text="Ver Clientes", command=ver_clientes)
btn_ver_clientes.grid(row=5, column=1, padx=10, pady=10)

ver_clientes_text = tk.Text(clientes_tab, height=10, width=60)
ver_clientes_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Filtros de busqueda avanzada
ttk.Label(productos_tab, text="Precio minimo:").grid(row=10, column=0, padx=10, pady=10)
entry_precio_min = ttk.Entry(productos_tab)
entry_precio_min.grid(row=10, column=1, padx=10, pady=10)

ttk.Label(productos_tab, text="Precio maximo:").grid(row=11, column=0, padx=10, pady=10)
entry_precio_max = ttk.Entry(productos_tab)
entry_precio_max.grid(row=11, column=1, padx=10, pady=10)

ttk.Button(productos_tab, text="Buscar Productos", command=buscar_productos_avanzada).grid(row=12, column=0, columnspan=2, pady=10)

# Mostrar ordenes
ordenes_tab = ttk.Frame(tab_control)
tab_control.add(ordenes_tab, text="Ordenes")

ttk.Label(ordenes_tab, text="ID Cliente:").grid(row=0, column=0, padx=10, pady=10)
entry_id_cliente_orden = ttk.Entry(ordenes_tab)
entry_id_cliente_orden.grid(row=0, column=1, padx=10, pady=10)

btn_mostrar_ordenes = ttk.Button(ordenes_tab, text="Mostrar ordenes", command=mostrar_ordenes)
btn_mostrar_ordenes.grid(row=1, column=0, padx=10, pady=10)

ordenes_text = tk.Text(ordenes_tab, height=10, width=60)
ordenes_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Reporte de Producto Mas Vendido
reporte_tab = ttk.Frame(tab_control)
tab_control.add(reporte_tab, text="Reporte")

btn_reporte_mas_vendido = ttk.Button(reporte_tab, text="Producto Mas Vendido", command=reporte_mas_vendido)
btn_reporte_mas_vendido.grid(row=0, column=0, padx=10, pady=10)

# Mostrar pestañas
tab_control.pack(expand=1, fill="both")

root.mainloop()
