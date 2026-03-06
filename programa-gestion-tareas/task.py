from datetime import datetime

class Task:

    def __init__(self, id, nombre, descripcion, fecha, prioridad, recordatorio, categoria):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.prioridad = prioridad
        self.recordatorio = recordatorio
        self.categoria = categoria
        self.estado = "Pendiente"

    def marcar_hecha(self):
        self.estado = "Hecha"
