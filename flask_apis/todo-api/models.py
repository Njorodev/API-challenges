class Todo:
    def __init__(self, id, task, completed=False):
        self.id = id
        self.task = task
        self.completed = completed

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed
        }
todos = []

