from task import Task


class TaskManager:

    def __init__(self):
        self.tareas = []
        self.contador = 1


    def crear_tarea(self, nombre, descripcion, fecha, prioridad):

        tarea = Task(
            self.contador,
            nombre,
            descripcion,
            fecha,
            prioridad
        )

        self.tareas.append(tarea)
        self.contador += 1

        return tarea


    def listar_tareas(self):
        return self.tareas


    def marcar_hecha(self, id_tarea):

        for tarea in self.tareas:

            if tarea.id == id_tarea:
                tarea.marcar_hecha()
                return True

        return False
