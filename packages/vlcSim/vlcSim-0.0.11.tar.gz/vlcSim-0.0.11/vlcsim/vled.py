import numpy as np
import math as m
from enum import Enum


class VLed:
    numberOfVLeds = 0
    statev = Enum("state", "IDLE BUSY")

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        nLedsX: int,
        nLedsY: int,
        ledPower: float,
        theta: float,
    ) -> None:
        self.__x = x
        self.__y = y
        self.__z = z
        self.__nLedsX = nLedsX
        self.__nLedsY = nLedsY
        self.__ledPower = ledPower
        self.__theta = theta
        self.__state = VLed.statev.IDLE
        self.__sliceTime = None

        self.__numberOfLeds = self.__nLedsX * self.__nLedsY
        self.__totalPower = self.__numberOfLeds * self.__ledPower
        self.__ml = -m.log10(2) / m.log10(m.cos(m.radians(theta)))

        self.__ID = VLed.numberOfVLeds
        VLed.numberOfVLeds += 1
        self.__position = np.array([x, y, z])

    @property
    def ID(self) -> int:
        return self.__ID

    @ID.setter
    def ID(self, value: int):
        self.__ID = value

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float):
        self.__x = value
        self.__position = np.array([self.__x, self.y, self.z])

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float):
        self.__y = value
        self.__position = np.array([self.x, self.__y, self.z])

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float):
        self.__z = value
        self.__position = np.array([self.x, self.y, self.__z])

    @property
    def nLedsX(self) -> int:
        return self.__nLedsX

    @nLedsX.setter
    def nLedsX(self, value: int):
        self.__nLedsX = value

    @property
    def nLedsY(self) -> int:
        return self.__nLedsY

    @nLedsY.setter
    def nLedsY(self, value: int):
        self.__nLedsY = value

    @property
    def ledPower(self) -> float:
        return self.__ledPower

    @ledPower.setter
    def ledPower(self, value: float):
        self.__ledPower = value

    @property
    def theta(self) -> float:
        return self.__theta

    @theta.setter
    def theta(self, value: float):
        self.__theta = value

    @property
    def numberOfLeds(self) -> int:
        return self.__numberOfLeds

    @property
    def totalPower(self) -> float:
        return self.__totalPower

    @totalPower.setter
    def totalPower(self, value: float):
        self.__totalPower = value

    @property
    def position(self):
        return self.__position

    @property
    def ml(self):
        return self.__ml

    @property
    def state(self):
        return self.__state

    def setIDLE(self):
        self.__state = VLed.statev.IDLE

    def setBUSY(self):
        self.__state = VLed.statev.BUSY

    @property
    def sliceTime(self):
        return self.__sliceTime

    @sliceTime.setter
    def sliceTime(self, value):
        self.__sliceTime = value
