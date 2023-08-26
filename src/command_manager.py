class CommandManager:
    def __init__(self) -> None:
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        self.undo_stack.append(command)
        command.execute()
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.undo_stack.pop()
            command.execute()
            self.undo_stack.append(command)
