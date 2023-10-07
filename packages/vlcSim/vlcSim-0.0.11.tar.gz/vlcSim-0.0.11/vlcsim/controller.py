from .scenario import *
from .connection import *
from enum import Enum


class Controller:
    status = Enum("status", "ALLOCATED NOT_ALLOCATED WAIT")
    nextStatus = Enum("nextStatus", "PAUSE FINISH RESUME IDLE RND_WAIT")

    def __init__(self, x, y, z, nGrids, rho) -> None:
        self.__scenario = Scenario(x, y, z, nGrids, rho)
        self.__allocator = None
        self.__allocationStatus = None
        # self.__activeConnections = [[]] * len(self.__scenario.vleds)

    @property
    def scenario(self):
        return self.__scenario

    @property
    def allocationStatus(self):
        return self.__allocationStatus

    @property
    def allocator(self):
        return self.__allocator

    @allocator.setter
    def allocator(self, allocator):
        self.__allocator = allocator

    def assignConnection(self, connection, time):
        # connection = Connection(id_connection, receiver)
        self.__allocationStatus, connection = self.__allocator(
            connection.receiver, connection, self.__scenario, self
        )
        connection.receiver.timeFirstConnected = time
        if self.__allocationStatus == Controller.status.ALLOCATED:
            index = self.APPosition(connection.AP)
            if len(self.__activeConnections[index]) == 0:
                connection.AP.setBUSY()
                self.__activeConnections[index].append(connection)
                return Controller.nextStatus.RESUME, time, connection
            else:
                self.__activeConnections[index].insert(
                    self.__activeConnection[index], connection
                )
                self.__activeConnection[index] += 1
                return Controller.nextStatus.PAUSE, time, connection
        elif self.__allocationStatus == Controller.status.NOT_ALLOCATED:
            return Controller.nextStatus.IDLE, time, connection
        elif self.__allocationStatus == Controller.status.WAIT:
            return Controller.nextStatus.RND_WAIT, time, connection
        else:
            raise ("Return status of allocatyion algorithm not supported")

    def pauseConnection(self, connection, time):
        receiver = connection.receiver
        index = self.APPosition(connection.AP)
        receiver.timeActive += connection.AP.sliceTime
        if len(self.__activeConnections[index]) > 1:
            self.__activeConnection[index] += 1
            self.__activeConnection[index] = self.__activeConnection[index] % len(
                self.__activeConnections[index]
            )
            connection = self.__activeConnections[index][self.__activeConnection[index]]
        return Controller.nextStatus.RESUME, time, connection

    def resumeConnection(self, connection, time):
        receiver = connection.receiver
        if receiver.goalTime < receiver.timeActive + connection.AP.sliceTime:
            return (
                Controller.nextStatus.FINISH,
                time + receiver.goalTime - receiver.timeActive,
                connection,
            )
        else:
            return (
                Controller.nextStatus.PAUSE,
                time + connection.AP.sliceTime,
                connection,
            )

    def unassignConnection(self, connection, time):
        index = self.APPosition(connection.AP)
        receiver = connection.receiver
        receiver.timeActive = receiver.goalTime
        receiver.timeFinished = time
        self.__activeConnections[index].pop(self.__activeConnection[index])
        if len(self.__activeConnections[index]) == 0:
            self.__activeConnection[index] = 0
            connection.AP.setIDLE()
            return Controller.nextStatus.IDLE, time, None
        self.__activeConnection[index] = self.__activeConnection[index] % len(
            self.__activeConnections[index]
        )
        if len(self.__activeConnections[index]) > 0:
            connection = self.__activeConnections[index][self.__activeConnection[index]]
            return Controller.nextStatus.RESUME, time, connection
        else:
            connection.AP.setIDLE()
            return Controller.nextStatus.IDLE, time, None

    def init(self):
        self.__activeConnections = []

        for i in range(len(self.__scenario.vleds) + len(self.__scenario.rfs)):
            self.__activeConnections.append([])
        self.__activeConnection = [0] * len(self.__activeConnections)

    def APPosition(self, ap):
        if isinstance(ap, VLed):
            return self.__scenario.vledsPositions[ap.ID]
        elif isinstance(ap, RF):
            return self.__scenario.rfsPositions[ap.ID]

    @property
    def activeConnections(self):
        return self.__activeConnections

    def numberOfActiveConnections(self, vLedID: int):
        return len(self.__activeConnections[vLedID])
