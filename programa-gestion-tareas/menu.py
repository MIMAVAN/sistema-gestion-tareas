from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidget,
    QTableWidgetItem, QComboBox, QMessageBox
)

from datetime import datetime
from task_manager import TaskManager


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.manager = TaskManager()

        self.setWindowTitle("Gestor de Tareas")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción")

        self.fecha_input = QLineEdit()
        self.fecha_input.setPlaceholderText("YYYY-MM-DD")

        self.prioridad_input = QComboBox()
        self.prioridad_input.addItems(["Alta", "Media", "Baja"])

        crear_btn = QPushButton("Crear tarea")
        crear_btn.clicked.connect(self.crear_tarea)

        marcar_btn = QPushButton("Marcar como hecha")
        marcar_btn.clicked.connect(self.marcar_tarea)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Fecha", "Prioridad", "Estado"]
        )

        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Descripción"))
        layout.addWidget(self.descripcion_input)

        layout.addWidget(QLabel("Fecha"))
        layout.addWidget(self.fecha_input)

        layout.addWidget(QLabel("Prioridad"))
        layout.addWidget(self.prioridad_input)

        layout.addWidget(crear_btn)
        layout.addWidget(marcar_btn)
        layout.addWidget(self.tabla)

        self.setLayout(layout)


    def crear_tarea(self):

        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        fecha_texto = self.fecha_input.text()
        prioridad = self.prioridad_input.currentText()

        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d")
        except:
            QMessageBox.warning(self, "Error", "Fecha inválida")
            return

        self.manager.crear_tarea(nombre, descripcion, fecha, prioridad)

        self.actualizar_tabla()


    def actualizar_tabla(self):

        tareas = self.manager.listar_tareas()

        self.tabla.setRowCount(len(tareas))

        for fila, tarea in enumerate(tareas):

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(tarea.id)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(tarea.nombre))
            self.tabla.setItem(
                fila, 2, QTableWidgetItem(tarea.fecha.strftime("%Y-%m-%d"))
            )
            self.tabla.setItem(fila, 3, QTableWidgetItem(tarea.prioridad))
            self.tabla.setItem(fila, 4, QTableWidgetItem(tarea.estado))


    def marcar_tarea(self):

        fila = self.tabla.currentRow()

        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione una tarea")
            return

        id_tarea = int(self.tabla.item(fila, 0).text())

        self.manager.marcar_hecha(id_tarea)

        self.actualizar_tabla()
