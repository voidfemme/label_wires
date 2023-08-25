class CommandManager:
    def __init__(self) -> None:
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        print(f"CommandManager executing command {command}.")
        self.undo_stack.append(command)
        print(
            f"CommandManager added a command to the stack. Undo stack size: {len(self.undo_stack)}"
        )
        command.execute()
        self.redo_stack.clear()
        print(
            f"CommandManager: Redo stack cleared. Redo stack size: {len(self.redo_stack)}"
        )

    def undo(self):
        print(
            f"CommandManager attempting to undo. Undo stack size: {len(self.undo_stack)}"
        )
        if self.undo_stack:
            command = self.undo_stack.pop()
            print(
                f"Popped command: {command}. New undo stack size: {len(self.undo_stack)}"
            )
            command.undo()
            self.redo_stack.append(command)
            print(
                f"Command added to redo stack. Redo stack size: {len(self.redo_stack)}"
            )
        else:
            print("Nothing to undo.")

    def redo(self):
        print(
            f"CommandManager attempting to redo. Redo stack size: {len(self.redo_stack)}"
        )
        if self.redo_stack:
            command = self.undo_stack.pop()
            print(
                f"Popped command: {command}. New undo stack size: {len(self.undo_stack)}"
            )
            command.execute()
            self.undo_stack.append(command)
            print(
                f"Command added back to stack. Redo stack size: {len(self.redo_stack)}"
            )
        else:
            print("Nothing to redo.")
