import pymysql
from pymysql import MySQLError
from PyQt5.QtWidgets import QMessageBox
from controller.reporte import generar_pdf_ultimo_registro

def conectar_base_datos():
    """Función para conectar a la base de datos."""
    try:
        conexion = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",  # Asegúrate de ingresar la contraseña correcta si es necesario
            database="Bibliotecapyqt"  # Verifica que esta base de datos exista
        )
        
        print('¡Conexión a la base de datos establecida!')
        
        return conexion

    except MySQLError as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None

class OperacionesDB:
    def __init__(self, conexion):
        self.conexion = conexion

    def nuevo_lectorr(self, ci, nombre, apellido, fecha_N, telefono, direccion):
        try:
            cur = self.conexion.cursor()
            sql = """
            INSERT INTO tlector (`CI`, `Nombre`, `Apellido`, `Fecha de Nacimiento`, `Telefono`, `Direccion`)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (ci, nombre, apellido, fecha_N, telefono, direccion))
            self.conexion.commit()
            print("Nuevo lector insertado con éxito.")
            return True  # Retorna True si todo fue exitoso
        except pymysql.MySQLError as e:
            print(f"Error al insertar nuevo lector: {e}")
            return False  # Retorna False si hubo un error
        finally:
            cur.close()
    
    def nuevo_libroo(self, titulo, autor, genero, edicion, año_publicado, cantidad):
        try:
            cur = self.conexion.cursor()
            id_disponible = 0  # Si no es necesario como parámetro dinámico, puedes quitar esto
            sql = """
                INSERT INTO tlibros (`Titulo`, `Autor`, `Genero`, `Edicion`, `Año Publicado`, `Cantidad`, `ID_Disponible`)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (titulo, autor, genero, edicion, año_publicado, cantidad, id_disponible))
            self.conexion.commit()
            print("Nuevo libro insertado con éxito.")
            return True  # Retorna True si se insertó correctamente
        except pymysql.MySQLError as e:
            print(f"Error al insertar nuevo libro: {e}")
            return False  # Retorna False en caso de error
        finally:
            if cur:
                cur.close()
            
    def buscar_lector(self, ci): 
        try:
            cur = self.conexion.cursor()
            # Consulta para buscar al lector y verificar préstamos
            sql = """
            SELECT 
                CONCAT(tlector.Nombre, ' ', tlector.Apellido) AS LectorNo, 
                tregprestamoslibro.ID_Estado, 
                TIMESTAMPDIFF(YEAR, tlector.`Fecha de Nacimiento`, CURDATE()) AS Edad
            FROM 
                tlector 
            LEFT JOIN 
                tregprestamoslibro 
            ON 
                tlector.CI = tregprestamoslibro.CI 
            WHERE 
                tlector.CI = %s AND tregprestamoslibro.ID_Estado = 1
            """
            cur.execute(sql, (ci,))
            resultado = cur.fetchone()
            
            if resultado:
                # Si hay un préstamo, devolvemos el nombre, la edad y el indicador de préstamo previo
                return (resultado[0], resultado[2], True)
            else:
                # Si no hay préstamo pero el lector existe, devolvemos el nombre y la edad
                sql = """
                SELECT 
                    CONCAT(Nombre, ' ', Apellido) AS LectorNo, 
                    TIMESTAMPDIFF(YEAR, `Fecha de Nacimiento`, CURDATE()) AS Edad 
                FROM 
                    tlector 
                WHERE 
                    CI = %s
                """
                cur.execute(sql, (ci,))
                resultado = cur.fetchone()
                return (resultado[0], resultado[1], False) if resultado else (None, None, False)
            
        except pymysql.MySQLError as e:
            print(f"Error al buscar el lector: {e}")
            return None, None, False
            
        finally:
            cur.close()

            
    def buscar_lector_reporte(self, ci): 
        try:
            cur = self.conexion.cursor()
            # Consulta para buscar al lector
            sql = """
            SELECT CONCAT(tlector.Nombre, ' ', tlector.Apellido) AS LectorNo
            FROM tlector
            WHERE tlector.CI = %s
            """
            cur.execute(sql, (ci,))  # Asegúrate de pasar ci como una tupla
            resultado = cur.fetchone()  # Busca solo un resultado
            if resultado:
                return resultado[0]  # Devuelve solo el nombre concatenado
            else:
                print("No se encontró un lector con ese CI.")
                return None
        except pymysql.MySQLError as e:
            print(f"Error al buscar el lector: {e}")
            return None  # En caso de error, devuelve None
        finally:
            cur.close()
            
    def obtener_datos_completos_lector(self, ci):
        try:
            cur = self.conexion.cursor()
            # Consulta para obtener todos los datos del lector
            sql = """
            SELECT CI, Nombre, Apellido, `Fecha de Nacimiento`, 
                Telefono, Direccion
            FROM tlector
            WHERE CI = %s
            """
            cur.execute(sql, (ci,))
            resultado = cur.fetchone()
            if resultado:
                # Devuelve los datos como un diccionario
                columnas = [col[0] for col in cur.description]
                return dict(zip(columnas, resultado))
            else:
                print("No se encontró un lector con ese CI.")
                return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener los datos del lector: {e}")
            return None
        finally:
            cur.close()
     
    
    def buscar_codigo(self, codigo):
        try:
            cur = self.conexion.cursor()
            sql = """
             SELECT CONCAT(u.Nombre, ' ', u.Apellido) AS LectorNo, l.Titulo, p.`Fecha de Devolucion`, p.Observaciones, E.Estado
            FROM tregprestamoslibro p
            JOIN tlector u ON u.CI = p.CI
            JOIN tlibros l ON l.ID_Libro = p.ID_Libro
            jOIN testado E on E.ID_Estado = p.ID_Estado
            WHERE p.Codigo = %s;
            """
            cur.execute(sql, (codigo,))
            resultado = cur.fetchall()
            return resultado
            
        except pymysql.MySQLError as e:
            print(f"Error al buscar el lector: {e}")
            return None  # En caso de error, devuelve None
        
        finally:
            cur.close()
            

    
    def listas_de_libros(self):
        try:
            cur = self.conexion.cursor()
            # Selecciona el título y la disponibilidad de todos los libros
            sql = "SELECT Titulo, ID_Disponible FROM tlibros"
            cur.execute(sql)
            resultado = cur.fetchall()
            return resultado  # Retorna una lista de tuplas (Titulo, ID_Disponible).
        except pymysql.MySQLError as e:
            print(f"Error al buscar los libros: {e}")
            return []  # Devuelve una lista vacía en caso de error.
        finally:
            cur.close()
                
    def listas_Testados(self):
        try:
            cur = self.conexion.cursor()
            sql = " SELECT Estado FROM testado"
            cur.execute(sql,)
            resultado = cur.fetchall()
            return [fila[0] for fila in resultado]
        except pymysql.MySQLError as e:
            print(f"Error al buscar el lector: {e}")
            return None  # En caso de error, devuelve None
        finally:
            cur.close()
    
    def obtener_id_libro(self, titulo):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT ID_Libro FROM TLibros WHERE Titulo = %s"
            cur.execute(sql, (titulo,))
            resultado = cur.fetchone()
            if resultado:
                return resultado[0]  # Devuelve el ID del libro
            else:
                print("No se encontró el libro.")
                return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener el ID del libro: {e}")
            return None
        finally:
            cur.close()
    
    def obtener_id_Estado(self, estado ):
        try:
            cur = self.conexion.cursor()
            sql = "select ID_Estado from testado where  estado = %s"
            cur.execute(sql, (estado))
            resultado = cur.fetchone()
            if resultado:
                return resultado[0]
            else:
                print("No se encontró el estado.")
                return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener el ID del estado: {e}")
            return None
        finally:
            cur.close()
    
    def Regis_Prestamos_de_libros(self, ci_lector, libros, Fecha_R, Fecha_D, cantidad):
        try:
            cur = self.conexion.cursor()
            # Obtener el ID del libro basado en el título
            id_libro = self.obtener_id_libro(libros)
            if id_libro is None:
                print("Error al obtener el ID del libro.")
                return False  # Retornar False si no se pudo obtener el ID del libro
            # Insertar el préstamo en la base de datos
            sql = """
                INSERT INTO TRegPrestamosLibro 
                    (`Fecha de Reserva`, `Fecha de Devolucion`, `Observaciones`, `CI`, `ID_Libro`, `Cantidad`, `ID_Estado`)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
            """
            estado = 1   # Ejemplo de estado inicial
            observaciones = None  # O puedes definir algo aquí si es necesario
            cur.execute(sql, (Fecha_R, Fecha_D, observaciones, ci_lector, id_libro, cantidad, estado))
            self.conexion.commit()
            print("Préstamo registrado con éxito.")
            
            # Obtener el último registro insertado usando LAST_INSERT_ID()
            cur.execute("SELECT * FROM TRegPrestamosLibro WHERE Codigo = LAST_INSERT_ID()")
            cur.execute("""
                    SELECT 
                        TRegPrestamosLibro.Codigo,
                        TRegPrestamosLibro.`Fecha de Reserva`,
                        TRegPrestamosLibro.`Fecha de Devolucion`,
                        TRegPrestamosLibro.CI,
                        TRegPrestamosLibro.ID_Libro,
                        TRegPrestamosLibro.Cantidad,
                        TRegPrestamosLibro.ID_Estado,
                        Tlector.Nombre,
                        Tlector.Apellido,
                        Tlibros.Titulo
                    FROM 
                        TRegPrestamosLibro
                    JOIN 
                        Tlector ON TRegPrestamosLibro.CI = Tlector.CI
                    JOIN 
                        Tlibros ON TRegPrestamosLibro.ID_Libro = Tlibros.ID_Libro
                    WHERE 
                        TRegPrestamosLibro.Codigo = LAST_INSERT_ID();
            """)
            ultimo_registro = cur.fetchone()
            print("Último registro insertado:")
            print(generar_pdf_ultimo_registro(ultimo_registro))
            return True  # Retornar True si la operación fue exitosa
        except pymysql.MySQLError as e:
            print(f"Error al registrar el préstamo: {e}")
            return False  # Retornar False en caso de error
        finally:
            cur.close()
    
    
    
    def actualizar_devolucion(self, codigo_D, fecha_Devol, estado, Observaciones):
        try:
            cur = self.conexion.cursor()

            # Obtener el ID del estado
            id_estado = 2
            if id_estado is None:
                print("Error al obtener el ID del Estado.")
                return False  # Error al obtener el ID del estado

            # Actualizar el registro
            sql = """ 
                UPDATE TRegPrestamosLibro 
                SET 
                    `Fecha de Devolucion` = %s,
                    Observaciones = %s,
                    ID_Estado = %s  
                WHERE Codigo = %s                  
            """
            cur.execute(sql, (fecha_Devol, Observaciones, id_estado, codigo_D))
            self.conexion.commit()
           
            # Verificar si se actualizó alguna fila
            if cur.rowcount > 0:
                print("Préstamo registrado con éxito.")
                return True  # Actualización exitosa
            else:
                print("No se encontró ningún registro para actualizar.")
                return False  # No se encontró el registro
            
        except pymysql.MySQLError as e:
            print(f"Error al registrar el préstamo: {e}")
            return False  # Error en la base de datos
        finally:
            cur.close()

    def total_lector(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT COUNT(CI) FROM tlector;"
            cur.execute(sql)
            total_registrados = cur.fetchone()[0]  
            return total_registrados
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
            
    def total_libro(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT SUM(Cantidad) FROM tlibros;"
            cur.execute(sql)
            total_registrados = cur.fetchone()[0]  
            return total_registrados
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
            
    def total_prestamos(self):    
        try:
            cur = self.conexion.cursor()
            sql = "SELECT SUM(ID_Estado)  FROM `tregprestamoslibro` WHERE ID_Estado = 1"
            cur.execute(sql)
            total_registrados = cur.fetchone()[0]  
            return total_registrados
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
    
    def total_devoluestos(self):    
        try:
            cur = self.conexion.cursor()
            sql = "SELECT SUM(ID_Estado)  FROM `tregprestamoslibro` WHERE ID_Estado = 2"
            cur.execute(sql)
            total_registrados = cur.fetchone()[0]  
            return total_registrados
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
    
    #Seccion Para el reporte        
    def todos_los_libros(self):
        try:
            with self.conexion.cursor() as cur:
                sql = "SELECT * FROM tlibros"
                cur.execute(sql)
                libros = cur.fetchall()
                return libros
        except pymysql.MySQLError as e:
            print(f"Error al obtener los libros: {e}")
        return []

    def todos_los_lectores(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM `tlector`"
            cur.execute(sql)
            total_los_lectores = cur.fetchall()  # Devuelve el total de lectores
            return total_los_lectores
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def todos_los_prestamos(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM `tregprestamoslibro` "
            cur.execute(sql)
            todos_los_prestamos = cur.fetchall() 
            return todos_los_prestamos
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def todas_las_devoluciones(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM `tregprestamoslibro` WHERE ID_Estado = 2"
            cur.execute(sql)
            todas_las_devoluciones = cur.fetchall()  # Devuelve el total de devoluciones
            return todas_las_devoluciones
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
       

    def libro_mas_prestado(self):
        try:
            cur = self.conexion.cursor()
            sql = """SELECT t.ID_Libro, l.titulo, l.autor, COUNT(t.ID_libro) AS total_prestamos
                     FROM tregprestamoslibro t
                     JOIN tlibros l ON t.ID_libro = l.ID_libro
                     GROUP BY t.ID_libro
                     ORDER BY total_prestamos DESC
                     LIMIT 5"""
            cur.execute(sql)
            libros_mas_prestados = cur.fetchall()  # Devuelve las filas con los libros más prestados
            return libros_mas_prestados
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def libros_disponibles(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM tlibros WHERE ID_Disponible = 0"
            cur.execute(sql)
            libros_disponibles = cur.fetchall()  # Devuelve el total de libros disponibles
            return libros_disponibles
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def libros_no_disponibles(self):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM tlibros WHERE ID_Disponible = 1"
            cur.execute(sql)
            libros_no_disponibles = cur.fetchall()  # Devuelve el total de libros no disponibles
            return libros_no_disponibles
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def libros_no_devueltos(self):
        try:
            cur = self.conexion.cursor()
            sql = """
            SELECT tr.Codigo , tr.`Fecha de Reserva`, tr.CI,tr.ID_Libro , tl.Titulo FROM 
                tregprestamoslibro tr 
                JOIN 
                    tlibros tl 
                ON 
                    tr.ID_Libro = tl.ID_Libro 
                WHERE 
                 tr.ID_Estado = 1;
            
            """
            cur.execute(sql)
            libros_no_devueltos = cur.fetchall() 
            return libros_no_devueltos
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()

    def lector_mas_frecuente(self):
        try:
            cur = self.conexion.cursor()
            sql = """SELECT tr.CI, CONCAT(tl.Nombre, ' ', tl.Apellido) AS Lector, COUNT(tr.CI) AS total_prestamos
                     FROM tregprestamoslibro tr
                     JOIN tlector tl ON tr.CI = tl.CI
                     GROUP BY tr.CI, tl.Nombre, tl.Apellido
                     ORDER BY total_prestamos DESC
                     LIMIT 5"""
            cur.execute(sql)
            lectores_frecuentes = cur.fetchall()  # Devuelve las filas con los lectores más frecuentes
            return lectores_frecuentes
        except pymysql.MySQLError as e:
            print(f"Error al obtener el total de registros: {e}")
            return 0
        finally:
            cur.close()
            
    def lector_con_multas(self):
        print()
        
    def obtener_datos_lector(self, ci):
        try:
            cur = self.conexion.cursor()
            sql = "SELECT * FROM tlector WHERE CI = %s"
            cur.execute(sql, (ci,))
            resultado = cur.fetchone()
            return resultado  # Devuelve todos los datos del lector
        except pymysql.MySQLError as e:
            print(f"Error al obtener los datos del lector: {e}")
            return None
        finally:
            cur.close()

    def obtener_prestamos_devueltos(self, ci):
        try:
            cur = self.conexion.cursor()
            sql = """
            SELECT Codigo, `Fecha de Reserva`, `Fecha de Devolucion`, Cantidad, Observaciones
            FROM tregprestamoslibro
            WHERE CI = %s AND ID_Estado = 1
            """
            cur.execute(sql, (ci,))
            return cur.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error al obtener préstamos devueltos: {e}")
            return []
        finally:
            cur.close()

    # Obtener préstamos pendientes
    def obtener_prestamos_pendientes(self, ci):
        try:
            cur = self.conexion.cursor()
            sql = """
            SELECT Codigo, `Fecha de Reserva`, `Fecha de Devolucion`, Cantidad, Observaciones
            FROM tregprestamoslibro
            WHERE CI = %s AND ID_Estado = 2
            """
            cur.execute(sql, (ci,))
            return cur.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error al obtener préstamos pendientes: {e}")
            return []
        finally:
            cur.close()        
            
         
    
def cerrar_conexion(conexion):
    """Función para cerrar la conexión a la base de datos."""
    if conexion:
        conexion.close()
        print('Conexión cerrada.')

