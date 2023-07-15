class EventSystem:
    def __init__(self) -> None:
        self._events = {}

    def subscribe(self, event_name: str, callback):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def publish(self, event_name: str, *args, **kwargs):
        if event_name not in self._events:
            return
        for callback in self._events[event_name]:
            callback(*args, **kwargs)
