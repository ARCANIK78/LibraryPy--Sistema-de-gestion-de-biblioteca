import sys
from PyQt5.QtWidgets import QApplication
from controller.controllador import ControladorPrincipalUI
from views.Biblioteca import Ui_MainWindow
from controller.mensaje import *
def main():

    app = QApplication(sys.argv)
    ventana = ControladorPrincipalUI()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
