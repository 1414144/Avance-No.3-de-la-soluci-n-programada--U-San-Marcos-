import tkinter as tk
from tkinter import messagebox
from datetime import datetime


inventario = []
total_perdidas = 0


def agregar_producto():
    global total_perdidas
    try:
        nombre = entry_nombre.get()
        cantidad = int(entry_cantidad.get())
        precio = float(entry_precio.get())
        fecha_texto = entry_fecha.get()

        fecha_vencimiento = datetime.strptime(fecha_texto, "%d/%m/%Y")
        fecha_hoy = datetime.now()

        estado = "DISPONIBLE"

        if fecha_vencimiento < fecha_hoy:
            estado = "VENCIDO"
            perdida = cantidad * precio
            total_perdidas += perdida

        producto = {
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "fecha": fecha_vencimiento,
            "estado": estado
        }

        inventario.append(producto)
        actualizar_lista()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Producto agregado")
    except ValueError:
        messagebox.showerror("Error", "Datos inválidos")


def actualizar_lista():
    lista_productos.delete(0, tk.END)
    for i, p in enumerate(inventario):
        lista_productos.insert(tk.END, f"{i+1}. {p['nombre']}")


def mostrar_detalle():
    try:
        index = lista_productos.curselection()[0]
        p = inventario[index]
        info = f"Nombre: {p['nombre']}\nCantidad: {p['cantidad']}\nPrecio: {p['precio']}\nFecha: {p['fecha'].strftime('%d/%m/%Y')}\nEstado: {p['estado']}"
        messagebox.showinfo("Detalle", info)
    except IndexError:
        messagebox.showwarning("Aviso", "Seleccione un producto")


def borrar_producto():
    global total_perdidas
    try:
        index = lista_productos.curselection()[0]
        p = inventario.pop(index)

        if p["estado"] == "VENCIDO":
            total_perdidas -= p["cantidad"] * p["precio"]

        actualizar_lista()
        messagebox.showinfo("Éxito", "Producto eliminado")
    except IndexError:
        messagebox.showwarning("Aviso", "Seleccione un producto")


def mostrar_perdidas():
    messagebox.showinfo("Pérdidas", f"Total: {total_perdidas}")


def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)


ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("500x400")


tk.Label(ventana, text="Nombre").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Cantidad").pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

tk.Label(ventana, text="Precio").pack()
entry_precio = tk.Entry(ventana)
entry_precio.pack()

tk.Label(ventana, text="Fecha (DD/MM/AAAA)").pack()
entry_fecha = tk.Entry(ventana)
entry_fecha.pack()


tk.Button(ventana, text="Agregar", command=agregar_producto).pack(pady=5)
tk.Button(ventana, text="Mostrar detalle", command=mostrar_detalle).pack(pady=5)
tk.Button(ventana, text="Borrar", command=borrar_producto).pack(pady=5)
tk.Button(ventana, text="Ver pérdidas", command=mostrar_perdidas).pack(pady=5)


lista_productos = tk.Listbox(ventana)
lista_productos.pack(fill=tk.BOTH, expand=True, pady=10)

ventana.mainloop()