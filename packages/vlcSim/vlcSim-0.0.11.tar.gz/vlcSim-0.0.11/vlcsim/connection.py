class Connection:
    def __init__(self, id, receiver) -> None:
        self.__id = id
        self.__ap = None
        self.__receiver = receiver
        self.__allocated = True

    @property
    def receiver(self):
        return self.__receiver

    @receiver.setter
    def receiver(self, value):
        self.__receiver = value

    @property
    def id(self):
        return self.__id

    @property
    def AP(self):
        return self.__ap

    @AP.setter
    def AP(self, ap):
        self.__ap = ap

    @property
    def allocated(self):
        return self.__allocated

    @allocated.setter
    def allocated(self, value):
        self.__allocated = value
