from task import Task


class TaskManager:

    def __init__(self):
        self.tareas = []
        self.categorias = ["General"]
        self.contador = 1


    def crear_tarea(self, nombre, descripcion, fecha, prioridad, recordatorio, categoria):

        tarea = Task(
            self.contador,
            nombre,
            descripcion,
            fecha,
            prioridad,
            recordatorio,
            categoria
        )

        self.tareas.append(tarea)
        self.contador += 1


    def listar_tareas(self):
        return self.tareas


    def marcar_hecha(self, id_tarea):

        for tarea in self.tareas:

            if tarea.id == id_tarea:
                tarea.marcar_hecha()
                return True

        return False


    def crear_categoria(self, nombre):

        if nombre not in self.categorias:
            self.categorias.append(nombre)


    def listar_categorias(self):
        return self.categorias


    def filtrar_por_categoria(self, categoria):

        resultado = []

        for tarea in self.tareas:

            if tarea.categoria == categoria:
                resultado.append(tarea)

        return resultado
