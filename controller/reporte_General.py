from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape 
from reportlab.lib.pagesizes import letter , A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from models.base_de_datos import conectar_base_datos, OperacionesDB
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QPushButton, QVBoxLayout, QWidget, QMessageBox
from reportlab.pdfgen import canvas
import datetime

titulo_estilo = ParagraphStyle(
            name='TituloGeneral',
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=20,
        )

subtitulo_estilo = ParagraphStyle(
            name='Subtitulo',
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=10,
        )

class GeneradorReportes(QMainWindow):
    def obtener_datos(self, consultas):
        """
        Obtiene los datos según las consultas seleccionadas.
        """
        datos = {}
        # Asegúrate de tener una conexión abierta a la base de datos
        dbBase = conectar_base_datos()
        operaciones = OperacionesDB(dbBase)
        
        
        for consulta in consultas:
            if consulta == "todos_los_libros":
                datos[consulta] = operaciones.todos_los_libros()
            elif consulta == "todos_los_lectores":
                datos[consulta] = operaciones.todos_los_lectores()
            elif consulta == "todos_los_prestamos":
                datos[consulta] = operaciones.todos_los_prestamos()
            elif consulta == "todas_las_devoluciones":
                datos[consulta] = operaciones.todas_las_devoluciones()
            elif consulta == "libro_mas_prestado":
                datos[consulta] = operaciones.libro_mas_prestado()
            elif consulta == "libros_disponibles":
                datos[consulta] = operaciones.libros_disponibles()
            elif consulta == "libros_no_disponibles":
                datos[consulta] = operaciones.libros_no_disponibles()
            elif consulta == "libros_no_devueltos":
                datos[consulta] = operaciones.libros_no_devueltos()
            elif consulta == "lector_mas_frecuente":
                datos[consulta] = operaciones.lector_mas_frecuente()
        return datos

        
    def generar_pdf(self, datos):
        nombre_reporte = "reporte_biblioteca.pdf"

        # Crear un documento PDF
        doc = SimpleDocTemplate(nombre_reporte, pagesize=landscape((1100, 600)))

        # Crear una lista para almacenar los elementos del documento
        content = []
        # Ruta de la imagen del banner
        ruta_banner = r"C:\Users\DELL\Documents\Tareas de universidad\Ingenieria software\sistema biblioteca\controller\banner.jpg"
        ancho_banner = 1000  # Ajusta el ancho según necesites
        alto_banner = 150   # Ajusta el alto según necesites
        
        try:
            # Agregar el banner como imagen
            banner = Image(ruta_banner, width=ancho_banner, height=alto_banner)
            content.append(banner)
            content.append(Spacer(1, 20))  # Espacio después del banner
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el banner: {e}")
            return
        
        titulo_general = "Reporte General de la Biblioteca"
        subtitulo_general = "Detalle completo de libros, préstamos, devoluciones y más"
        fecha_creacion = f"Fecha de creación: {datetime.datetime.now().strftime('%d/%m/%Y')}"
        
        # Estilo para los párrafos (títulos fuera de la tabla)
        styles = getSampleStyleSheet()
        titulo_style = styles['Title']
        normal_style = styles['Normal']
        content.append(Paragraph(titulo_general, titulo_estilo))
        content.append(Paragraph(subtitulo_general, subtitulo_estilo))
        content.append(Paragraph(fecha_creacion, normal_style))
        # Títulos de las columnas y datos de las consultas
        consultas_encabezados = {
            "todos_los_libros": {
                "titulo": "Listado de Todos los Libros",
                "encabezados": ["ID_Libro", "Titulo", "Autor", "Genero", "Edicion", "Año Publicado", "Cantidad", "ID_Disponible"]
            },
            "todos_los_prestamos": {
                "titulo": "Todos los Préstamos",
                "encabezados": ["Codigo", "Fecha de Reserva", "Fecha de Devolucion", "Observaciones", "CI","ID_Libro","Cantidad","ID_Estado"]
            },
             "todos_los_lectores": {
                "titulo": "Todos los Lectores",
                "encabezados": ["CI", "Nombre", "Apellido", "Fecha de Nacimiento", "Telefono", "Direccion"]
            },
             "todas_las_devoluciones": {
             "titulo": "Listado de Todas las Devoluciones",
             "encabezados": ["Codigo", "Fecha de Reserva", "Fecha de Devolucion", "Observaciones", "CI","ID_Libro","Cantidad","ID_Estado"]
            }, 
             "libro_mas_prestado": {
                "titulo": "Libro Más Prestado",
                "encabezados": ["ID_Libro", "Titulo", "Autor", "Cantidad de Préstamos"]
            },
            "libros_disponibles": {
                "titulo": "Libros Disponibles",
                "encabezados": ["ID_Libro", "Titulo", "Autor", "Genero", "Edicion", "Año Publicado", "Cantidad Disponible"]
            },
            "libros_no_disponibles": {
                "titulo": "Libros No Disponibles",
                "encabezados": ["ID_Libro", "Titulo", "Autor", "Genero", "Edicion", "Año Publicado", "Cantidad Disponible","Estado"]
            },
            "libros_no_devueltos": {
                "titulo": "Libros No Devueltos",
                "encabezados": ["Codigo", "Fecha de Préstamo","CI", "ID_libro", "Titulo" ]
            },
            "lector_mas_frecuente": {
                "titulo": "Lector Más Frecuente",
                "encabezados": ["CI", "Nombre", "Cantidad de Préstamos"]
            }
        }

        # Iterar sobre cada consulta y sus resultados
        for consulta, resultados in datos.items():
            config = consultas_encabezados.get(consulta, {})
            titulo = config.get("titulo", consulta)
            encabezados = config.get("encabezados", [])
            
            if content:
                content.append(PageBreak())

            # Agregar el título como un párrafo
            content.append(Paragraph(titulo, titulo_style))
            content.append(Spacer(1, 12))  # Espacio entre título y tabla

            if not resultados:
                # Si no hay resultados, mostrar mensaje
                content.append(Paragraph("Sin datos para mostrar.", normal_style))
                content.append(Spacer(1, 12))  # Espacio después del mensaje
                continue

            # Crear la tabla con encabezados y datos
            datos_tabla = [encabezados]  # Añadir encabezados como primera fila
            for fila in resultados:
                fila_convertida = [str(valor) if isinstance(valor, datetime.date) else str(valor) for valor in fila]
                datos_tabla.append(fila_convertida)

            # Crear la tabla de ReportLab
            tabla = Table(datos_tabla)

            # Estilo de la tabla
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            # Añadir la tabla al contenido
            
            content.append(tabla)
            content.append(Spacer(1, 24))  # Espacio entre tablas

        # Construir el documento
        try:
            doc.build(content)
            QMessageBox.information(self, "Reporte Generado", f"El reporte se ha guardado como {nombre_reporte}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el reporte: {e}")