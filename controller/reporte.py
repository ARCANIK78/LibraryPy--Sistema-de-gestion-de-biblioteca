from models.base_de_datos import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generar_pdf_ultimo_registro(ultimo_registro):
    """
    Genera un PDF con los datos del último registro en formato de factura.
    :param ultimo_registro: Tupla con los datos del último registro.
    """
    codigo = ultimo_registro[0]
    
    # Define el nombre y tamaño del archivo PDF
    archivo_pdf = f"controller/factura_prestar/C-{codigo}.pdf"
    
    # Crear el documento PDF con tamaño personalizado
    doc = SimpleDocTemplate(archivo_pdf, pagesize=(400, 700))
    
    # Obtener estilos predefinidos
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]
    
    # Título de la factura
    title = Paragraph("Comprobante de Préstamo de Libros", title_style)
    
    # Detalles de la factura
    factura_info = [
        ["Número de Comprobante", f"C-{codigo}"],
        ["Fecha de Emisión", ultimo_registro[1]],
    ]
    
    # Tabla de detalle
    data = [
        ["Campo", "Valor"],  # Encabezados de columna
        ["Código", ultimo_registro[0]],
        ["Fecha de Reserva", ultimo_registro[1]],
        ["Fecha de Devolución", ultimo_registro[2]],
        ["CI Lector", ultimo_registro[3]],
        ["Nombre Lector", f"{ultimo_registro[7]} {ultimo_registro[8]}"],
        ["ID del Libro", ultimo_registro[4]],
        ["Título del Libro", ultimo_registro[9]],
    ]
    
    # Crear la tabla de detalles
    table = Table(data, colWidths=[120, 250])

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
    
    # Aplicar los estilos a la tabla
    table.setStyle(style)
    
    # Crear el encabezado de la factura (Nombre de la empresa o servicio)
    header_info = Paragraph("<b>Biblioteca XYZ</b><br/>Dirección: Calle Mamore, Ciudad : Trinidad", normal_style)
    
    # Lista de elementos que se incluirán en el PDF
    elements = [header_info, Spacer(1, 10), title, Spacer(1, 10)]  # Espacios entre los elementos
    elements += [Table(factura_info, colWidths=[120, 250]), Spacer(1, 10)]  # Información de la factura
    elements += [table]  # Tabla con los detalles del registro
    
    # Construir el PDF
    doc.build(elements)

    print(f"PDF generado: {archivo_pdf}")
