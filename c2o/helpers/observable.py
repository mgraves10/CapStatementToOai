__all__ = ["Observable", "Observer", "ElementObserver", "ValueObserver"]


class Observable:
    def __init__(self) -> None:
        self._observers = []

    def register_observer(self, observer) -> None:
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, observable) -> None:
        observable.register_observer(self)

    def resolve_observer_type(self):
        return ''.join(
            filter(lambda x: x != "object",
                   map(lambda x: x.__name__, self.__class__.__mro__)))

    def discriminator(self, *args):
        return False

    def action(self, *args):
        pass

    def resolve_discriminators(self):
        pass

    def notify(self, observable, *args, **kwargs) -> None:
        if self.discriminator(*args):
            self.action(*args)
            print(self.resolve_observer_type(), "Got", args, kwargs, "From", observable)


class ElementObserver(Observer):
    pass


class ValueObserver(Observer):
    pass


class TypeObserver(Observer):
    pass