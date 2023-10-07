import math as m
from enum import Enum


class RF:
    numberOfRFs = 0
    stater = Enum("state", "IDLE BUSY")

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        bf: float = 5e6,
        pf: float = 40,
        BERf: float = 10e-5,
        Af: float = 10.0,
        Ef: float = 1.0,
        R_awgn: float = 1 * 10 ** (-174 / 10),
        N_rf: int = 10,
        nFactor_rf: float = 1.0,
        A: float = 0.1e6,
    ) -> None:
        self.__x = x
        self.__y = y
        self.__z = z
        self.__bf = bf
        self.__pf = pf
        self.__BERf = BERf
        self.__Af = Af
        self.__Ef = Ef
        self.__R_awgn = R_awgn
        self.__N_rf = N_rf
        self.__nFactor_rf = nFactor_rf
        self.__A = A
        self.__state = RF.stater.IDLE
        self.__sliceTime = None

        self.__pif = -1.5 / m.log(5 * self.__BERf)
        self.__ID = RF.numberOfRFs
        RF.numberOfRFs += 1

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, value):
        self.__ID = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value):
        self.__z = value

    @property
    def bf(self):
        return self.__bf

    @bf.setter
    def bf(self, value):
        self.__bf = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def BERf(self):
        return self.__BERf

    @BERf.setter
    def BERf(self, value):
        self.__BERf = value

    @property
    def Af(self):
        return self.__Af

    @Af.setter
    def Af(self, value):
        self.__Af = value

    @property
    def Ef(self):
        return self.__Ef

    @Ef.setter
    def Ef(self, value):
        self.__Ef = value

    @property
    def R_awgn(self):
        return self.__R_awgn

    @R_awgn.setter
    def R_awgn(self, value):
        self.__R_awgn = value

    @property
    def pif(self):
        return self.__pif

    @pif.setter
    def pif(self, value):
        self.__pif = value

    @property
    def N_rf(self):
        return self.__N_rf

    @N_rf.setter
    def N_rf(self, value):
        self.__N_rf = value

    @property
    def nFactor_rf(self):
        return self.__nFactor_rf

    @nFactor_rf.setter
    def nFactor_rf(self, value):
        self.__nFactor_rf = value

    @property
    def A(self):
        return self.__A

    @A.setter
    def A(self, value):
        self.__A = value

    def setIDLE(self):
        self.__state = RF.stater.IDLE

    def setBUSY(self):
        self.__state = RF.stater.BUSY

    @property
    def sliceTime(self):
        return self.__sliceTime

    @sliceTime.setter
    def sliceTime(self, value):
        self.__sliceTime = value
