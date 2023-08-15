from abc import abstractmethod,ABC

class CarService(ABC):

    @abstractmethod
    def add_car(self):
        pass

    @abstractmethod
    def delete_car(self):
        pass

    @abstractmethod
    def update_car(self):
        pass

    @abstractmethod
    def get_all_car(self):
        pass

    @abstractmethod
    def get_car(self):
        pass

    @abstractmethod
    def transfer_car(self):
        pass

