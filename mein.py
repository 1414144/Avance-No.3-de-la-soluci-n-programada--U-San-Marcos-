import tkinter as tk
from tkinter import messagebox
from datetime import datetime

nombres_productos = []
cantidades_productos = []
precios_productos = []
fechas_vencimiento = []
total_productos = 0
contador_productos = 0

def definir_cantidad():
    global total_productos
    try:
        total_productos = int(entry_total.get())

        if total_productos <= 0:
            messagebox.showwarning("Advertencia", "Digite un número mayor que 0")
            return

        label_estado.config(
            text=f"Debe ingresar {total_productos} productos"
        )

        entry_total.config(state="disabled")
        boton_definir.config(state="disabled")

    except:
        messagebox.showerror("Error", "Ingrese un número válido")


def guardar_producto():
    global contador_productos
    if total_productos == 0:
        messagebox.showwarning("Advertencia", "Primero indique cuántos productos va a registrar")
        return
    nombre = entry_nombre.get()
    cantidad = entry_cantidad.get()
    precio = entry_precio.get()
    fecha = entry_fecha.get()
    if nombre == "" or cantidad == "" or precio == "" or fecha == "":
        messagebox.showwarning("Advertencia", "Complete todos los datos")
        return
    try:
        cantidad = int(cantidad)
        precio = float(precio)
        fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y")
        nombres_productos.append(nombre)
        cantidades_productos.append(cantidad)
        precios_productos.append(precio)
        fechas_vencimiento.append(fecha_convertida)
        contador_productos += 1
        area_texto.insert(
            tk.END,
            f"Producto {contador_productos}: {nombre} | Cantidad: {cantidad} | Precio: {precio} | Vence: {fecha}\n"
        )

        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)

        label_estado.config(
            text=f"Lleva {contador_productos} de {total_productos} productos"
        )

        if contador_productos == total_productos:
            messagebox.showinfo("Información", "Ya registró todos los productos")
            boton_guardar.config(state="disabled")

    except:
        messagebox.showerror("Error", "Revise cantidad, precio y fecha (dd/mm/aaaa)")


def calcular_perdidas():
    if len(nombres_productos) == 0:
        messagebox.showwarning("Advertencia", "No hay productos guardados")
        return

    hoy = datetime.now()
    total_perdidas = 0

    area_resultados.delete("1.0", tk.END)
    area_resultados.insert(tk.END, "REPORTE DE PRODUCTOS\n")
    area_resultados.insert(tk.END, "-----------------------------\n")

    for i in range(len(nombres_productos)):
        nombre = nombres_productos[i]
        cantidad = cantidades_productos[i]
        precio = precios_productos[i]
        fecha_venc = fechas_vencimiento[i]

        if hoy > fecha_venc:
            perdida = cantidad * precio
            total_perdidas = total_perdidas + perdida
            estado = "VENCIDO"
        else:
            perdida = 0
            estado = "DISPONIBLE"

        area_resultados.insert(
            tk.END,
            f"Nombre: {nombre}\nCantidad: {cantidad}\nPrecio: {precio}\n"
            f"Vence: {fecha_venc.strftime('%d/%m/%Y')}\nEstado: {estado}\n"
            f"Pérdida: {perdida}\n-----------------------------\n"
        )

    area_resultados.insert(tk.END, f"TOTAL DE PÉRDIDAS: {total_perdidas}\n")

def limpiar_todo():
    global total_productos, contador_productos

    nombres_productos.clear()
    cantidades_productos.clear()
    precios_productos.clear()
    fechas_vencimiento.clear()

    total_productos = 0
    contador_productos = 0

    entry_total.config(state="normal")
    boton_definir.config(state="normal")

    entry_total.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)

    area_texto.delete("1.0", tk.END)
    area_resultados.delete("1.0", tk.END)

    boton_guardar.config(state="normal")

    label_estado.config(text="Sistema listo para registrar productos")


ventana = tk.Tk()
ventana.title("Control de Productos y Fechas de Vencimiento")
ventana.geometry("750x650")
ventana.config(bg="#dff6ff")

titulo = tk.Label(
    ventana,
    text="Control de Productos",
    font=("Arial", 16, "bold"),
    bg="#dff6ff"
)
titulo.pack(pady=10)

frame_total = tk.Frame(ventana, bg="#dff6ff")
frame_total.pack(pady=5)

label_total = tk.Label(frame_total, text="Cantidad de productos a registrar:", bg="#dff6ff")
label_total.grid(row=0, column=0, padx=5, pady=5)

entry_total = tk.Entry(frame_total)
entry_total.grid(row=0, column=1, padx=5, pady=5)

boton_definir = tk.Button(frame_total, text="Definir cantidad", command=definir_cantidad)
boton_definir.grid(row=0, column=2, padx=5, pady=5)

frame_datos = tk.Frame(ventana, bg="#dff6ff")
frame_datos.pack(pady=10)

tk.Label(frame_datos, text="Nombre:", bg="#dff6ff").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_datos)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_datos, text="Cantidad:", bg="#dff6ff").grid(row=1, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(frame_datos)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_datos, text="Precio:", bg="#dff6ff").grid(row=2, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_datos)
entry_precio.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_datos, text="Fecha vencimiento (dd/mm/aaaa):", bg="#dff6ff").grid(row=3, column=0, padx=5, pady=5)
entry_fecha = tk.Entry(frame_datos)
entry_fecha.grid(row=3, column=1, padx=5, pady=5)

boton_guardar = tk.Button(ventana, text="Guardar producto", command=guardar_producto, bg="#90e0ef")
boton_guardar.pack(pady=10)

label_estado = tk.Label(ventana, text="Sistema listo para registrar productos", bg="#dff6ff", fg="blue")
label_estado.pack()

tk.Label(ventana, text="Productos registrados:", bg="#dff6ff", font=("Arial", 11, "bold")).pack()
area_texto = tk.Text(ventana, height=10, width=80)
area_texto.pack(pady=5)

frame_botones = tk.Frame(ventana, bg="#dff6ff")
frame_botones.pack(pady=10)

boton_calcular = tk.Button(frame_botones, text="Calcular pérdidas", command=calcular_perdidas, bg="#ade8f4")
boton_calcular.grid(row=0, column=0, padx=10)

boton_limpiar = tk.Button(frame_botones, text="Limpiar todo", command=limpiar_todo, bg="#ffadad")
boton_limpiar.grid(row=0, column=1, padx=10)

tk.Label(ventana, text="Resultados:", bg="#dff6ff", font=("Arial", 11, "bold")).pack()
area_resultados = tk.Text(ventana, height=12, width=80)
area_resultados.pack(pady=5)

ventana.mainloop()
