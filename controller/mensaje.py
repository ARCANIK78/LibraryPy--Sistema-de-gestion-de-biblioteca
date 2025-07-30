from PyQt5.QtWidgets import QMessageBox

def mostrar_mensaje(self, titulo, mensaje, icono):
        """
        Muestra un mensaje en pantalla.

        Args:
            titulo (str): El título de la ventana del mensaje.
            mensaje (str): El contenido del mensaje.
            icono (QMessageBox.Icon): El tipo de icono a mostrar.

        Returns:
            None
        """
        msg = QMessageBox()
        msg.setIcon(icono)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()