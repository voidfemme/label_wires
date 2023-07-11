class CommandManager:
    def __init__(self) -> None:
        self.stack = []
        self.undo_stack = []

    def execute(self, command):
        self.stack.append(command)
        command.execute()
        self.undo_stack.clear()

    def undo(self):
        if self.stack:
            command = self.stack.pop()
            command.undo()
            self.undo_stack.append(command)

    def redo(self):
        if self.undo_stack:
            command = self.stack.pop()
            command.execute()
            self.stack.append(command)

    # add a function to protect the stack from growing too large
