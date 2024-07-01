import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

# Parte del primer código
# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación con tkinter")

# Crear la tabla
tabla = ttk.Treeview(root, columns=('RUT', 'Nombre', 'Apellido', 'Profesión', 'País', 'Estado Emocional', 'UTM Easting', 'UTM Northing', 'UTM Zone Number', 'UTM Zone Letter'))
tabla.heading('#0', text='ID')
tabla.heading('RUT', text='RUT')
tabla.heading('Nombre', text='Nombre')
tabla.heading('Apellido', text='Apellido')
tabla.heading('Profesión', text='Profesión')
tabla.heading('País', text='País')
tabla.heading('Estado Emocional', text='Estado Emocional')
tabla.heading('UTM Easting', text='UTM Easting')
tabla.heading('UTM Northing', text='UTM Northing')
tabla.heading('UTM Zone Number', text='UTM Zone Number')
tabla.heading('UTM Zone Letter', text='UTM Zone Letter')
tabla.pack(padx=10, pady=10)

# Botones para cargar archivo, modificar dato, eliminar dato y guardar información
frame_botones = tk.Frame(root)
frame_botones.pack(padx=10, pady=10)

# Función para cargar un archivo CSV y mostrarlo en la tabla
def cargar_archivo():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filename:
        # Limpiar tabla si ya hay datos
        limpiar_tabla()

        # Leer el archivo CSV y mostrarlo en la tabla
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                tabla.insert('', 'end', values=row)

# Función para limpiar la tabla
def limpiar_tabla():
    tabla.delete(*tabla.get_children())

# Función para abrir la ventana de edición y modificar datos
def abrir_ventana_modificar():
    selected_item = tabla.focus()
    if selected_item:
        datos_seleccionados = tabla.item(selected_item, 'values')
        ventana_modificar = tk.Toplevel(root)
        ventana_modificar.title("Modificar Dato")

        # Campos de entrada para los datos seleccionados
        tk.Label(ventana_modificar, text="Nombre:").grid(row=0, column=0)
        entry_nombre = tk.Entry(ventana_modificar)
        entry_nombre.insert(0, datos_seleccionados[1])
        entry_nombre.grid(row=0, column=1)

        tk.Label(ventana_modificar, text="Apellido:").grid(row=1, column=0)
        entry_apellido = tk.Entry(ventana_modificar)
        entry_apellido.insert(0, datos_seleccionados[2])
        entry_apellido.grid(row=1, column=1)

        tk.Label(ventana_modificar, text="Profesión:").grid(row=2, column=0)
        entry_profesion = tk.Entry(ventana_modificar)
        entry_profesion.insert(0, datos_seleccionados[3])
        entry_profesion.grid(row=2, column=1)

        tk.Label(ventana_modificar, text="País:").grid(row=3, column=0)
        entry_pais = tk.Entry(ventana_modificar)
        entry_pais.insert(0, datos_seleccionados[4])
        entry_pais.grid(row=3, column=1)

        tk.Label(ventana_modificar, text="Estado Emocional:").grid(row=4, column=0)
        entry_estado = tk.Entry(ventana_modificar)
        entry_estado.insert(0, datos_seleccionados[5])
        entry_estado.grid(row=4, column=1)

        # Función para guardar los cambios
        def guardar_cambios():
            nueva_data = (
                datos_seleccionados[0],  # RUT (no editable)
                entry_nombre.get(),
                entry_apellido.get(),
                entry_profesion.get(),
                entry_pais.get(),
                entry_estado.get(),
                *datos_seleccionados[6:]  # Resto de datos (no editables)
            )
            tabla.item(selected_item, values=nueva_data)
            ventana_modificar.destroy()

        # Botón para guardar cambios
        btn_guardar = tk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=5, columnspan=2)

# Función para eliminar un dato seleccionado
def eliminar_dato():
    selected_item = tabla.selection()
    if selected_item:
        for item in selected_item:
            tabla.delete(item)

# Botones del primer código
btn_cargar_archivo = tk.Button(frame_botones, text="Cargar archivo", command=cargar_archivo)
btn_cargar_archivo.pack(side=tk.LEFT, padx=5)

btn_modificar_dato = tk.Button(frame_botones, text="Modificar dato", command=abrir_ventana_modificar)
btn_modificar_dato.pack(side=tk.LEFT, padx=5)

btn_eliminar_dato = tk.Button(frame_botones, text="Eliminar dato", command=eliminar_dato)
btn_eliminar_dato.pack(side=tk.LEFT, padx=5)

# Función para convertir UTM a latitud y longitud (del segundo código)
def convertir_utm_a_lat_long(utm_easting, utm_northing, utm_zone_number, utm_zone_letter):
    # Utiliza pyproj para la conversión
    p = Proj(proj='utm', zone=utm_zone_number, ellps='WGS84', datum='WGS84')
    lon, lat = p(utm_easting, utm_northing, inverse=True)
    return lat, lon

# Función para guardar la información en la base de datos (del segundo código)
def guardar_informacion():
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()

    try:
        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos (
                RUT TEXT,
                Nombre TEXT,
                Apellido TEXT,
                Profesion TEXT,
                Pais TEXT,
                Estado_Emocional TEXT,
                UTM_Easting REAL,
                UTM_Northing REAL,
                UTM_Zone_Number INTEGER,
                UTM_Zone_Letter TEXT
            )
        ''')

        # Guardar los datos de la tabla tkinter en la base de datos
        for child in tabla.get_children():
            values = tabla.item(child)['values']
            rut, nombre, apellido, profesion, pais, estado, utm_easting, utm_northing, utm_zone_number, utm_zone_letter = values[:10]

            # Convertir UTM a latitud y longitud
            lat, lon = convertir_utm_a_lat_long(float(utm_easting), float(utm_northing), utm_zone_number, utm_zone_letter)

            # Insertar en la base de datos
            cursor.execute('''
                INSERT INTO datos (RUT, Nombre, Apellido, Profesion, Pais, Estado_Emocional, UTM_Easting, UTM_Northing, UTM_Zone_Number, UTM_Zone_Letter, Latitud, Longitud)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (rut, nombre, apellido, profesion, pais, estado, utm_easting, utm_northing, utm_zone_number, utm_zone_letter, lat, lon))

        # Confirmar cambios y cerrar conexión
        conn.commit()
        messagebox.showinfo("Guardar Información", "Los datos han sido guardados correctamente en la base de datos.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e}")

    finally:
        cursor.close()
        conn.close()

# Botón para guardar información (del segundo código)
btn_guardar_informacion = tk.Button(frame_botones, text="Guardar información", command=guardar_informacion)
btn_guardar_informacion.pack(side=tk.LEFT, padx=5)

# Configurar Combobox de países (del primer código)
tk.Label(root, text="Seleccione país:").pack(padx=10, pady=10)
country_combobox = ttk.Combobox(root, state="readonly")
country_combobox.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
#esto es una prueba para agregar el archivo csv y despues agregarlo al codigo normal 

