from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidget,
    QTableWidgetItem, QComboBox, QMessageBox
)

from datetime import datetime, timedelta
from task_manager import TaskManager
from PySide6.QtCore import QTimer

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.manager = TaskManager()

        self.setWindowTitle("Gestor de Tareas")
        self.resize(600, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.verificar_recordatorios)
        self.timer.start(60000)  # revisa cada minuto

        layout = QVBoxLayout()

        self.categoria_input = QComboBox()
        self.categoria_input.addItems(self.manager.listar_categorias())

        self.recordatorio_input = QComboBox()
        self.recordatorio_input.addItems([
            "Sin recordatorio",
            "Cada 1 minuto",
            "Cada 5 minutos",
            "Cada 10 minutos"
        ])

        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar tarea...")
        self.buscar_input.textChanged.connect(self.buscar_tarea)

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

        self.nueva_categoria_input = QLineEdit()
        self.nueva_categoria_input.setPlaceholderText("Nueva categoría")

        crear_categoria_btn = QPushButton("Crear categoría")
        crear_categoria_btn.clicked.connect(self.crear_categoria)

        marcar_btn = QPushButton("Marcar como hecha")
        marcar_btn.clicked.connect(self.marcar_tarea)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Fecha", "Prioridad", "Categoría", "Estado"]
        )

        self.alerta = QLabel("")
        layout.addWidget(self.alerta)

        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Descripción"))
        layout.addWidget(self.descripcion_input)

        layout.addWidget(QLabel("Fecha"))
        layout.addWidget(self.fecha_input)

        layout.addWidget(QLabel("Prioridad"))
        layout.addWidget(self.prioridad_input)

        layout.addWidget(QLabel("Frecuencia de recordatorio"))
        layout.addWidget(self.recordatorio_input)

        layout.addWidget(QLabel("Categoría"))
        layout.addWidget(self.categoria_input)

        layout.addWidget(crear_btn)
        layout.addWidget(marcar_btn)

        layout.addWidget(QLabel("Nueva categoría"))
        layout.addWidget(self.nueva_categoria_input)
        layout.addWidget(crear_categoria_btn)

        layout.addWidget(QLabel("Buscar"))
        layout.addWidget(self.buscar_input)
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def crear_categoria(self):

        nombre = self.nueva_categoria_input.text()

        if nombre == "":
            return

        self.manager.crear_categoria(nombre)

        self.categoria_input.clear()
        self.categoria_input.addItems(self.manager.listar_categorias())


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

        recordatorio = self.recordatorio_input.currentText()
        categoria = self.categoria_input.currentText()

        self.manager.crear_tarea(
            nombre,
            descripcion,
            fecha,
            prioridad,
            recordatorio,
            categoria
        )

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
            self.tabla.setItem(fila, 4, QTableWidgetItem(tarea.categoria))
            self.tabla.setItem(fila, 5, QTableWidgetItem(tarea.estado))


    def marcar_tarea(self):

        fila = self.tabla.currentRow()

        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione una tarea")
            return

        id_tarea = int(self.tabla.item(fila, 0).text())

        self.manager.marcar_hecha(id_tarea)

        self.actualizar_tabla()

    def buscar_tarea(self):

        texto = self.buscar_input.text().lower()
        tareas = self.manager.listar_tareas()

        tareas_filtradas = []

        for tarea in tareas:
            if texto in tarea.nombre.lower():
                tareas_filtradas.append(tarea)

        self.tabla.setRowCount(len(tareas_filtradas))

        for fila, tarea in enumerate(tareas_filtradas):

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(tarea.id)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(tarea.nombre))
            self.tabla.setItem(
                fila, 2, QTableWidgetItem(tarea.fecha.strftime("%Y-%m-%d"))
            )
            self.tabla.setItem(fila, 3, QTableWidgetItem(tarea.prioridad))
            self.tabla.setItem(fila, 4, QTableWidgetItem(tarea.estado))


    def verificar_recordatorios(self):

        ahora = datetime.now()

        for tarea in self.manager.listar_tareas():

            if tarea.estado != "Hecha":

                diferencia = (tarea.fecha - ahora).total_seconds()

                if diferencia <= 0:
                    QMessageBox.information(
                        self,
                        "Recordatorio",
                        f"La tarea '{tarea.nombre}' debe realizarse ahora"
                    )
                else:
                    self.alerta.setText(f"Recordatorio: {tarea.nombre} pendiente")
