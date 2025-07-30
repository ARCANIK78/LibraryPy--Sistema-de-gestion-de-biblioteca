from models.base_de_datos import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import datetime

def generar_reporte_lector(lector_datos, prestamos_devueltos, prestamos_pendientes):
    # Verifica que los datos del lector estén presentes
    if not lector_datos:
        print("No se encontraron datos del lector.")
        return

    # Acceso a los datos mediante las claves del diccionario
    ci = lector_datos.get('CI', 'No disponible')
    nombre = lector_datos.get('Nombre', 'No disponible')
    apellido = lector_datos.get('Apellido', 'No disponible')
    fecha_nacimiento = lector_datos.get('Fecha de Nacimiento', 'No disponible')
    telefono = lector_datos.get('Telefono', 'No disponible')
    direccion = lector_datos.get('Direccion', 'No disponible')

    # Definir la ruta y nombre del archivo PDF
    carpeta_reportes = "reportes"
    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)  # Crear carpeta si no existe

    archivo_pdf = os.path.join(carpeta_reportes, f"reporte_lector_{ci}.pdf")
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)

    # Obtener estilos predefinidos
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Título del reporte
    title = Paragraph(f"Reporte del Lector: {nombre} {apellido}", title_style)

    # Datos del lector
    datos_tabla = [
        ["CI", ci],
        ["Nombre", nombre],
        ["Apellido", apellido],
        ["Fecha de Nacimiento", fecha_nacimiento],
        ["Teléfono", telefono],
        ["Dirección", direccion],
    ]

    # Crear la tabla con los datos del lector
    tabla_datos = Table(datos_tabla, colWidths=[120, 250])

    # Estilos para la tabla
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Fondo gris para el encabezado
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Color del texto en el encabezado
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Alineación a la izquierda
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Fuente en negrita para el encabezado
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),  # Fuente normal para el resto
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Espaciado debajo del encabezado
        ("TOPPADDING", (0, 1), (-1, -1), 10),  # Espaciado encima de las filas
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Agregar líneas de cuadrícula
    ])
    tabla_datos.setStyle(style)

   # Información de los préstamos devueltos
    prestamos_info = [["ID", "FechaPrestamo", "FechaLimite", "Comentarios"]]
    if prestamos_devueltos:
        prestamos_info += [[str(item['ID']), item['FechaPrestamo'], item['FechaLimite'], item['Comentarios']] for item in prestamos_devueltos]
    else:
        prestamos_info.append(["No hay préstamos devueltos."] * 4)

    tabla_devueltos = Table(prestamos_info, colWidths=[80, 100, 100, 200])

     # Información de los préstamos devueltos
    prestamos_info = [["ID", "FechaPrestamo", "FechaLimite", "Comentarios"]]
    if prestamos_devueltos:
        # Validación para cada registro
        for item in prestamos_devueltos:
            id_ = str(item.get('ID', 'No disponible'))
            fecha_prestamo = item.get('FechaPrestamo', 'No disponible')
            fecha_limite = item.get('FechaLimite', 'No disponible')
            comentarios = item.get('Comentarios', 'No disponible')
            prestamos_info.append([id_, fecha_prestamo, fecha_limite, comentarios])
    else:
        prestamos_info.append(["No hay préstamos devueltos."] * 4)

    tabla_devueltos = Table(prestamos_info, colWidths=[80, 100, 100, 200])

    # Estilos para la tabla de préstamos devueltos
    tabla_devueltos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    titulo_devueltos = Paragraph("Préstamos Devueltos", styles["Heading2"])
    # Información de los préstamos pendientes
    prestamos_pendientes_info = [["ID", "FechaPrestamo", "FechaLimite", "Comentarios"]]
    if prestamos_pendientes:
        # Validación para cada registro
        for item in prestamos_pendientes:
            id_ = str(item.get('ID', 'No disponible'))
            fecha_prestamo = item.get('FechaPrestamo', 'No disponible')
            fecha_limite = item.get('FechaLimite', 'No disponible')
            comentarios = item.get('Comentarios', 'No disponible')
            prestamos_pendientes_info.append([id_, fecha_prestamo, fecha_limite, comentarios])
    else:
        prestamos_pendientes_info.append(["No hay préstamos pendientes."] * 4)

    tabla_pendientes = Table(prestamos_pendientes_info, colWidths=[80, 100, 100, 200])

    titulo_pendientes = Paragraph("Préstamos Pendientes", styles["Heading2"])
    
    # Estilos para la tabla de préstamos pendientes
    tabla_pendientes.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Compilar elementos para el PDF
    elements = [title, Spacer(1, 12), tabla_datos, Spacer(1, 12),titulo_pendientes,   tabla_devueltos, Spacer(1, 12),titulo_devueltos, tabla_pendientes]

    # Generar PDF
    try:
        doc.build(elements)
        print(f"Reporte generado exitosamente: {archivo_pdf}")
    except Exception as e:
        print(f"Error al generar el reporte: {e}")