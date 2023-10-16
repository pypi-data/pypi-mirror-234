from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def connect(self) -> None:
        # connect to Controller
        ...
    
    @abstractmethod
    def get_all(self) -> None:
        # get all devices
        ...
    
    @abstractmethod
    def get_sockets(self) -> None:
        ...


class Hase(Controller):
    def connect(self) -> None:
        print("Connecting")
    
    def get_all(self) -> None:
        ...
    
    def get_sockets(self) -> None:
        ...

    def check_pwrjee(self) -> None:
        ...

