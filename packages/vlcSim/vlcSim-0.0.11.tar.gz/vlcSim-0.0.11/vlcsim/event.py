from enum import Enum


class Event:
    event = Enum("event", "ARRIVE DEPARTURE PAUSE RESUME NEXT_CONNECTION_TRY")

    def __init__(self, type=None, time=-1, id_connection=-1):
        self.__time = time
        self.__id_connection = id_connection
        if type == None:
            self.__type = Event.event.ARRIVE
        else:
            self.__type = type
        self.__connection = None

    @property
    def type(self):
        return self.__type

    @property
    def time(self):
        return self.__time

    @property
    def id_connection(self):
        return self.__id_connection

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, value):
        self.__connection = value
