from django.dispatch import Signal


test_event = Signal()


class EventManager:
    _signals = {}

    @classmethod
    def get_signal(cls, event_name):
        if event_name not in cls._signals:
            cls._signals[event_name] = Signal()
        return cls._signals[event_name]


def listen_to(event_name):
    """Decorator to connect a function to a dynamic event signal."""

    def decorator(func):
        def wrapper(instance, *args, **kwargs):
            signal = EventManager.get_signal(event_name)
            signal.connect(func, sender=instance)
            return func(instance, *args, **kwargs)

        return wrapper

    return decorator
