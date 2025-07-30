from models.base_de_datos import conectar_base_datos, OperacionesDB
from views.Biblioteca import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QMessageBox, QDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
import views.resource_rc
from .mensaje import mostrar_mensaje
from .reporte_General import GeneradorReportes
from .Reporte_Lectores import generar_reporte_lector
from views.ventanaPendientes import Ui_Dialog
import datetime

class VentanaPendientes(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

class ControladorPrincipalUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dbBase = conectar_base_datos()
        self.opraciones = OperacionesDB(self.dbBase)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Iconos_only.hide()#para ocultar la barra de iconos 
        self.ui.stackedWidget.setCurrentIndex(0)#Para que muestre la pagina Dasboard primero
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.btn_Home.setCheckable(True) 
        
        #Establecer la fecha actual   
        self.ui.dateEdit_9.setDate(QDate.currentDate())
        self.ui.dateEdit_10.setDate(QDate.currentDate())
        
        #Seccion de las ubicaciones de las paginas     
        self.ui.btn_Home.clicked.connect(self.switch_to_dashboard_page)
        self.ui.bt_Home.clicked.connect(self.switch_to_dashboard_page)
        
        self.ui.btn_usuario.clicked.connect(self.switch_to_Lector_page)
        self.ui.bt_usuario.clicked.connect(self.switch_to_Lector_page)
        
        self.ui.btn_libros.clicked.connect(self.switch_to_Libros_page)
        self.ui.bt_libros.clicked.connect(self.switch_to_Libros_page)
        
        self.ui.btn_prestamos.clicked.connect(self.switch_to_Prestamos_page)
        self.ui.bt_prestamos.clicked.connect(self.switch_to_Prestamos_page)
        
        self.ui.pushButton_6.clicked.connect(self.switch_to_deovluciones_page)
        self.ui.bt_devoluciones.clicked.connect(self.switch_to_deovluciones_page)
        
        self.ui.pushButton_7.clicked.connect(self.switch_to_reportes)
        self.ui.bt_devoluciones_2.clicked.connect(self.switch_to_reportes)
        
        self.ui.pushButton_5.clicked.connect(self.switc_to_reporte_general)
        self.ui.pushButton_8.clicked.connect(self.switc_to_reporte_lector)
        #Botones para enviar datos
        
        lectorr = RegLector()
        self.ui.btn_reg_Lector.clicked.connect(lambda: lectorr.Reg_lector(
        self.ui.lineEdit_7.text().strip(),
        self.ui.lineEdit_8.text().strip(),
        self.ui.lineEdit_9.text().strip(),
        self.ui.dateEdit.date().toString('yyyy-MM-dd'),
        self.ui.lineEdit_11.text().strip(),
        self.ui.lineEdit_12.text().strip(),
        self.opraciones,
        self.ui
        ))
        libro = RegLibro()
        self.ui.btn_reg_libros.clicked.connect(lambda: libro.Reg_Libros(
        self.ui.lineEdit_10.text().strip(),  # Título
        self.ui.lineEdit_13.text().strip(),  # Autor
        self.ui.lineEdit_14.text().strip(),  # Género
        self.ui.lineEdit_15.text().strip(),  # Edición
        self.ui.dateEdit_2.date().toString('yyyy-MM-dd'),  # Año publicado
        self.ui.spinBox.value(),  # Cantidad
        self.opraciones,  # Operaciones
        self.ui  # Objeto de la interfaz
       ))

       # llector = Lector(self.ui, self.opraciones)
        libros = Libros(self.ui, self.opraciones)
        self.lector = Lector(self.ui, self.opraciones)

        # Conectar el botón al método buscar_lector
        self.ui.pushButton_19.clicked.connect(self.lector.ConultarLector)
        # Conectar los botones a las clases
     #   self.ui.pushButton_19.clicked.connect(llector.buscar_lector)

        self.lista_estado()  # Esta sigue siendo la misma si se necesita
        self.registro_prestamos = RegPrestamo(self.ui, self.opraciones)
        
        self.libros = Libros(self.ui, self.opraciones)
        libros.cargar_libros()
        # Conectar el comboBox_3 para la selección de libro
        self.ui.comboBox_3.currentIndexChanged.connect(self.libros.seleccionar_libro)

        
        # Aquí debes conectar al método registrar_prestamo de la instancia 'registro_prestamos'
        self.ui.btn_reg_prestamos.clicked.connect(self.registro_prestamos.registrar_prestamo)
        self.ui.comboBox_3.currentIndexChanged.connect(libros.seleccionar_libro)

        # Crear instancias de las clases
        self.buscar_codigo = Buscar_Codigo(self.ui, self.opraciones)
        self.devoluciones_de_libros = Devoluciones_De_Libros(self.ui, self.opraciones)

        # Conectar botones a métodos
        self.ui.pushButton_3.clicked.connect(self.buscar_codigo.ConulstarPrestamos)
        self.ui.pushButton_4.clicked.connect(self.devoluciones_de_libros.actuailizar_devolucion)

        
        #datos no editables
        self.ui.spinBox_5.setValue(1)#cantidad de libros
        self.ui.spinBox_5.setDisabled(True)
        self.ui.lineEdit_31.setDisabled(True)#Nombre y apellido Prestamos
        self.ui.lineEdit_4.setDisabled(True)#NombreApellido Devolucion
        self.ui.lineEdit_5.setDisabled(True)#Titulo de libro de Devolucion
        self.ui.comboBox.setDisabled(True)#Estado de prestamos
       # self.ui.comboBox_3.currentIndexChanged.connect(self.Seleccionar_libro)

        #Ecargado de abrir la ventana secundaria
        self.ui.pushButton_2.clicked.connect(self.abrir_ventana_pendientes)
        
        #para reprtes generales
        self.reportes = GeneradorReportes()
        self.ui.pushButton_9.clicked.connect(self.generar_reporte)
        
        #para reporte de lector
        self.ui.pushButton_21.clicked.connect(self.buscar_CI_reorte)
        self.ui.pushButton_10.clicked.connect(self.generar_reporte_lector)
        
        self.actualizar_totales()
        
    def switch_to_dashboard_page(self):
        self.actualizar_totales()
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def switch_to_Lector_page(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        
    def switch_to_Libros_page(self):
        self.ui.stackedWidget.setCurrentIndex(4)
    
    def switch_to_Prestamos_page(self):

        libros = Libros(self.ui, self.opraciones)
        libros.cargar_libros()
        # Conectar el evento de selección de libro al método 'seleccionar_libro'
        self.ui.comboBox_3.currentIndexChanged.connect(libros.seleccionar_libro)

    # Cambiar a la página de prés
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def switch_to_deovluciones_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        
    def switch_to_reportes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
    #Paginas de reportes    
    def switc_to_reporte_general(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)       
    
    def switc_to_reporte_lector(self):    
        self.ui.stackedWidget_2.setCurrentIndex(1)
    
    def actualizar_totales(self):
        # Obtener los datos de los libros, lectores, préstamos y devoluciones
        dato_libros = self.opraciones.total_libro()
        datoLector = self.opraciones.total_lector()
        datos_prestamos = self.opraciones.total_prestamos()
        datos_devuelto = self.opraciones.total_devoluestos()
        # Actualizar los labels con los datos obtenidos
        self.ui.label_38.setText(str(dato_libros))        # Total libros
        self.ui.label_59.setText(str(datoLector))         # Total lectores
        self.ui.label_41.setText(str(datos_prestamos))    # Total préstamos
        self.ui.label_29.setText(str(datos_devuelto))     # Total devoluciones


    def abrir_ventana_pendientes(self):
        self.ventana_pendientes = VentanaPendientes()
        self.ventana_pendientes.exec_()  # Muestra como diálogo modal 
    
    
    def generar_reporte(self):
        """
        Genera el reporte basado en los checkboxes seleccionados.
        """
        seleccionados = []
        if self.ui.checkBox.isChecked():
            seleccionados.append("todos_los_libros")
        if self.ui.checkBox_2.isChecked():
            seleccionados.append("todos_los_lectores")
        if self.ui.checkBox_3.isChecked():
            seleccionados.append("todos_los_prestamos")
        if self.ui.checkBox_4.isChecked():
            seleccionados.append("todas_las_devoluciones")
        if self.ui.checkBox_5.isChecked():
            seleccionados.append("libro_mas_prestado")
        if self.ui.checkBox_7.isChecked():
            seleccionados.append("libros_disponibles")
        if self.ui.checkBox_6.isChecked():
            seleccionados.append("libros_no_disponibles")
        if self.ui.checkBox_8.isChecked():
            seleccionados.append("libros_no_devueltos")
        if self.ui.checkBox_9.isChecked():
            seleccionados.append("lector_mas_frecuente")          

        if not seleccionados:
            QMessageBox.warning(self, "Error", "Selecciona al menos una consulta para generar el reporte.")
            return

        datos = self.reportes.obtener_datos(seleccionados)

        if datos:
            self.reportes.generar_pdf(datos)
            QMessageBox.information(self, "Éxito", "Reporte generado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudieron obtener datos para el reporte.")
            
    def buscar_CI_reorte(self):
        ci = self.ui.lineEdit_33.text()
        datosCI = self.opraciones.buscar_lector_reporte(ci)
        if datosCI:
            self.ui.lineEdit_6.setText(datosCI)
        else:
            mostrar_mensaje(self, "Error", "No se encontró un lector con ese CI.", QMessageBox.Icon.Critical)
            self.ui.lineEdit_6.clear()
            self.ui.lineEdit_33.clear()   
            
             
    def generar_reporte_lector(self):
        """
        Genera el reporte de un lector con sus datos personales,
        préstamos devueltos y pendientes.
        """
        ci = self.ui.lineEdit_33.text()
        if not ci:
            mostrar_mensaje(self, "Error", "Por favor, ingresa un CI válido.", QMessageBox.Icon.Warning)
            return

        # Obtener datos del lector
        lector_datos = self.opraciones.obtener_datos_lector(ci)
        print("Este es aquiiii", lector_datos)
        if not lector_datos:
            mostrar_mensaje(self, "Error", "No se encontró un lector con ese CI.", QMessageBox.Icon.Critical)
            return

        # Convertir la fecha de nacimiento
        if isinstance(lector_datos[3], datetime.date):
            fecha_nacimiento = lector_datos[3].strftime("%d-%m-%Y")
        else:
            fecha_nacimiento = lector_datos[3]

        # Obtener préstamos devueltos y pendientes
        prestamos_devueltos = self.opraciones.obtener_prestamos_devueltos(ci)
        prestamos_pendientes = self.opraciones.obtener_prestamos_pendientes(ci)

        if prestamos_devueltos is None or prestamos_pendientes is None:
            mostrar_mensaje(self, "Error", "Hubo un problema al obtener los datos de préstamos.", QMessageBox.Icon.Critical)
            return

        # Transformar datos de préstamos devueltos
        prestamos_devueltos_procesados = [
            {
                "ID": p[0],
                "FechaPrestamo": p[1].strftime("%d-%m-%Y") if isinstance(p[1], datetime.date) else p[1],
                "FechaDevolucion": p[2].strftime("%d-%m-%Y") if isinstance(p[2], datetime.date) else p[2],
                "FechaLimite": p[3].strftime("%d-%m-%Y") if isinstance(p[3], datetime.date) else p[3],  # Asegúrate de incluir FechaLimite
                "Comentarios": p[4] if p[4] else "Sin comentarios"
            }
            for p in prestamos_devueltos
        ]

        # Transformar datos de préstamos pendientes
        prestamos_pendientes_procesados = [
            {
                "ID": p[0],
                "FechaPrestamo": p[1].strftime("%d-%m-%Y") if isinstance(p[1], datetime.date) else p[1],
                "FechaDevolucion": p[2].strftime("%d-%m-%Y") if isinstance(p[2], datetime.date) else p[2],
                "FechaLimite": p[3].strftime("%d-%m-%Y") if isinstance(p[3], datetime.date) else p[3],  # Asegúrate de incluir FechaLimite
                "Comentarios": p[4] if p[4] else "Sin comentarios"
            }
            for p in prestamos_pendientes
        ]

        # Generar PDF del reporte
        generar_reporte_lector(
            lector_datos={
                "CI": lector_datos[0],
                "Nombre": lector_datos[1],
                "Apellido": lector_datos[2],
                "Fecha de Nacimiento": fecha_nacimiento,
                "Telefono": lector_datos[4],
                "Direccion": lector_datos[5],
            },
            prestamos_devueltos=prestamos_devueltos_procesados,
            prestamos_pendientes=prestamos_pendientes_procesados
        )
        mostrar_mensaje(self, "Éxito", "Reporte generado exitosamente.", QMessageBox.Icon.Information)
        

        
    #Estado del libro //Ubicado en Devolucion       
    def lista_estado(self):
        datosestado = self.opraciones.listas_Testados()
        if datosestado:
            for estados in datosestado:
                self.ui.comboBox.addItem(estados)
                   
#CmpRegtrarLibro
class RegLector():
    def Reg_lector(self, nombre, apellido, ci, fecha_N, telefono, direccion, opraciones, ui):
        if not nombre or not apellido or not ci or not telefono or not direccion:
            mostrar_mensaje(None, "Error", "Todos los campos son obligatorios. Por favor, complete todos los datos.", QMessageBox.Icon.Warning)
            return
        regLector = opraciones.nuevo_lectorr(ci, nombre, apellido, fecha_N, telefono, direccion)
        if regLector:  
            mostrar_mensaje(None, "Éxito", "Se registró al lector con éxito", QMessageBox.Icon.Information)
            ui.lineEdit_7.clear()  # Nombre
            ui.lineEdit_8.clear()  # Apellido
            ui.lineEdit_9.clear()  # CI
            ui.lineEdit_11.clear() # Teléfono
            ui.lineEdit_12.clear() # Dirección
            ui.dateEdit.setDate(QDate.currentDate())  # Restablecer fecha al día actual
        else: 
            mostrar_mensaje(None, "Error", "Hubo un problema al registrar al lector", QMessageBox.Icon.Critical)
            
#CmpRegLibro           
class RegLibro():
    def Reg_Libros(self, titulo, autor, genero, edicion, año_publicado, cantidad, opraciones, ui):
        if not titulo or not autor or not genero or not edicion or not año_publicado or not cantidad:
            mostrar_mensaje(None, "Error", "Todos los campos son obligatorios. Por favor, complete todos los datos.", QMessageBox.Icon.Warning)
            return
        rglibro = opraciones.nuevo_libroo(titulo, autor, genero, edicion, año_publicado, cantidad)
        if rglibro:
            mostrar_mensaje(None, "Éxito", "Se registró el libro con éxito", QMessageBox.Icon.Information)
            ui.lineEdit_10.clear()  # Título
            ui.lineEdit_13.clear()  # Autor
            ui.lineEdit_14.clear()  # Género
            ui.lineEdit_15.clear()  # Edición
            ui.dateEdit_2.setDate(QDate.currentDate())  # Restablecer fecha al día actual
            ui.spinBox.setValue(0)  # Restablecer cantidad a 0
        else:
            mostrar_mensaje(None, "Error", "Hubo un problema al registrar el libro", QMessageBox.Icon.Warning)
      
#CmpRegPrestamosLibro
# Clase para manejar las operaciones de Lector
class Lector:
    def __init__(self, ui, operaciones):
        self.ui = ui
        self.opraciones = operaciones

    def ConultarLector(self):
        ci = self.ui.lineEdit_30.text()
        try:
            datosCI, edad, ha_prestado = self.opraciones.buscar_lector(ci)
            print(datosCI, edad)
            
            if datosCI:
                self.ui.lineEdit_31.setText(datosCI)  # Muestra el nombre del lector
                
                if edad is not None and edad < 10:
                    mostrar_mensaje(
                        self.ui,
                        "Error",
                        f"El lector '{datosCI}' no puede realizar préstamos porque es menor de 10 años (Edad: {edad} años).",
                        QMessageBox.Icon.Critical
                    )
                    self.ui.lineEdit_30.clear()
                    self.ui.lineEdit_31.clear()
                
                elif ha_prestado:
                    mostrar_mensaje(
                        self.ui,
                        "Información",
                        f"El lector '{datosCI}' ya ha realizado un préstamo anteriormente.",
                        QMessageBox.Icon.Critical
                    )
                    self.ui.lineEdit_30.clear()
                    self.ui.lineEdit_31.clear()
            else:
                mostrar_mensaje(
                    self.ui,
                    "Error",
                    "No se encontró un lector con ese CI.",
                    QMessageBox.Icon.Critical
                )
                self.ui.lineEdit_30.clear()
        except Exception as e:
            print(f"Error al buscar lector: {e}")

            
class Libros:
    def __init__(self, ui, operaciones):
        self.ui = ui
        self.opraciones = operaciones

    def cargar_libros(self):
        datostitulos = self.opraciones.listas_de_libros()
        if datostitulos:
            self.ui.comboBox_3.clear()
            for titulo, disponible in datostitulos:
                # Añadir título al comboBox y guardar 'disponible' como dato adicional
                self.ui.comboBox_3.addItem(titulo, disponible)
        else:
            print("No hay libros disponibles.")
    def seleccionar_libro(self):
        indice = self.ui.comboBox_3.currentIndex()
        disponible = self.ui.comboBox_3.itemData(indice)
        
        # Depuración: Verifica los valores que están siendo seleccionados
        print(f"Índice seleccionado: {indice}, Disponible: {disponible}")
        if disponible == 1:  # Si '1' significa que no está disponible
            self.cargar_libros()
            QMessageBox.warning(self.ui.comboBox_3, "Libro no disponible", "Este libro no está disponible.")
        else:
            print("Libro disponible.")  # Procede con la lógica para libros disponibles.
    
class RegPrestamo:
    def __init__(self, ui, operaciones):
        self.ui = ui
        self.opraciones = operaciones

    def registrar_prestamo(self):
        ci_lector = self.ui.lineEdit_30.text()
        NyA = self.ui.lineEdit_31.text()
        libros = self.ui.comboBox_3.currentText()
        Fecha_R = self.ui.dateEdit_9.date()
        Fecha_D = self.ui.dateEdit_10.date()
        cantidad = self.ui.spinBox_5.value()

        if not ci_lector or not NyA or not libros:
            mostrar_mensaje(self, "Advertencia", "Por favor, completa todos los campos obligatorios.", QMessageBox.Icon.Warning)
            return
        
        # Verificar rango de fechas
        dias_diferencia = Fecha_R.daysTo(Fecha_D)
        if dias_diferencia > 10:
            mostrar_mensaje(self, "Error", "No puedes seleccionar más de 10 días de préstamo.", QMessageBox.Icon.Critical)
            return
        elif dias_diferencia <= 0:
            mostrar_mensaje(self, "Error", "La fecha de devolución debe ser posterior a la fecha de inicio.", QMessageBox.Icon.Critical)
            return

        Fecha_R_str = Fecha_R.toString('yyyy-MM-dd')
        Fecha_D_str = Fecha_D.toString('yyyy-MM-dd')

        # Registrar el préstamo
        resultado = self.opraciones.Regis_Prestamos_de_libros(ci_lector, libros, Fecha_R_str, Fecha_D_str, cantidad)
        
        if resultado:
            mostrar_mensaje(self, "Éxito", "El préstamo se ha registrado con éxito.", QMessageBox.Icon.Information)
            self.ui.lineEdit_30.clear()
            self.ui.lineEdit_31.clear()
        else:
            mostrar_mensaje(self, "Error", "Hubo un problema al registrar el préstamo.", QMessageBox.Icon.Critical)
            
#CmpRegDevolucion 
class Buscar_Codigo:
    def __init__(self, ui, operaciones):
        self.ui = ui
        self.operaciones = operaciones
    def ConulstarPrestamos(self):
        codigo = self.ui.lineEdit.text()
        datoCodigo = self.operaciones.buscar_codigo(codigo)
        if datoCodigo:
            lector, titulo, fecha_d, Observaciones, Estado = datoCodigo[0]
            self.ui.lineEdit_4.setText(lector)
            self.ui.lineEdit_5.setText(titulo)
            self.ui.comboBox.setEditText(Estado)
            self.ui.lineEdit_3.setText(Observaciones)
            self.ui.dateEdit_11.setDate(fecha_d)
        else:
            mostrar_mensaje(
                self.ui, 
                "Error", 
                "No se encontró el código. Vuelve a intentarlo.", 
                QMessageBox.Icon.Critical
            )
            self.limpiar_campos()

    def limpiar_campos(self):
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_3.clear()

class Devoluciones_De_Libros:
    def __init__(self, ui, operaciones):
        self.ui = ui
        self.operaciones = operaciones
    def actuailizar_devolucion(self):
        codigo_D = self.ui.lineEdit.text()
        fecha_Devol = self.ui.dateEdit_11.date().toString('yyyy-MM-dd')
        estado = self.ui.comboBox.currentText()
        Observaciones = self.ui.lineEdit_3.text()

        if not codigo_D or not estado or not fecha_Devol:
            mostrar_mensaje(
                self.ui, 
                "Advertencia", 
                "Por favor, completa todos los campos obligatorios.", 
                QMessageBox.Icon.Warning
            )
            return

        if estado == "Devuelto":
            mostrar_mensaje(
                self.ui, 
                "Error", 
                "El libro ya fue devuelto.", 
                QMessageBox.Icon.Warning
            )
            self.limpiar_campos()
            return

        resultado = self.operaciones.actualizar_devolucion(codigo_D, fecha_Devol, estado, Observaciones)
        if resultado:
            mostrar_mensaje(
                self.ui, 
                "Éxito", 
                "La devolución del libro se registró correctamente.", 
                QMessageBox.Icon.Information
            )
        else:
            mostrar_mensaje(
                self.ui, 
                "Error", 
                "No se pudo registrar la devolución del libro. Intenta nuevamente.", 
                QMessageBox.Icon.Critical
            )

        self.limpiar_campos()

    def limpiar_campos(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()


