import math as m
import numpy as np
import decimal


class Receiver:
    receiversCreated = 0

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        aDet: float,
        ts: float,
        index: float,
        fov: float,
        q: float = 1.6e-19,
        s: float = 0.54,
        b: float = 10e6,
        ibg: float = 5.1e-3,
        cb: float = 1.38e-23,
        tk: float = 298.0,
        a: float = 1.0,
        gv: float = 10.0,
        n: float = 1.12e-6,
        fr: float = 1.5,
        gm: float = 3e-2,
        i1: float = 0.562,
        i2: float = 0.0868,
    ) -> None:
        decimal.getcontext().prec = 14
        self.__x = x
        self.__y = y
        self.__z = z
        self.__aDet = aDet
        self.__ts = ts
        self.__index = index
        self.__fov = fov
        self.__q = q
        self.__s = s
        self.__b = b
        self.__ibg = ibg
        self.__cb = cb
        self.__tk = tk
        self.__a = a
        self.__gv = gv
        self.__n = n
        self.__fr = fr
        self.__gm = gm
        self.__i1 = i1
        self.__i2 = i2

        self.__timeFirstConnected = None
        self.__goalTime = None
        self.__timeActive = 0
        self.__timeFinished = None

        self.__gCon = (index**2) / (m.sin(m.radians(fov)) ** 2)
        self.__position = np.array([x, y, z])
        self.__ID = Receiver.receiversCreated
        Receiver.receiversCreated += 1

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

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float):
        self.__y = value

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float):
        self.__z = value

    @property
    def aDet(self) -> float:
        return self.__aDet

    @aDet.setter
    def aDet(self, value: float):
        self.__aDet = value

    @property
    def ts(self) -> float:
        return self.__ts

    @ts.setter
    def ts(self, value: float):
        self.__ts = value

    @property
    def index(self) -> float:
        return self.__index

    @index.setter
    def index(self, value: float):
        self.__index = value

    @property
    def fov(self) -> float:
        return self.__fov

    @fov.setter
    def fov(self, value: float):
        self.__fov = value

    @property
    def gCon(self) -> float:
        return self.__gCon

    @property
    def position(self):
        return self.__position

    @property
    def q(self):
        return self.__q

    @q.setter
    def q(self, value):
        self.__q = value

    @property
    def s(self):
        return self.__s

    @s.setter
    def s(self, value):
        self.__s = value

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value

    @property
    def ibg(self):
        return self.__ibg

    @ibg.setter
    def ibg(self, value):
        self.__ibg = value

    @property
    def cb(self):
        return self.__cb

    @cb.setter
    def cb(self, value):
        self.__cb = value

    @property
    def tk(self):
        return self.__tk

    @tk.setter
    def tk(self, value):
        self.__tk = value

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value

    @property
    def gv(self):
        return self.__gv

    @gv.setter
    def gv(self, value):
        self.__gv = value

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    @property
    def fr(self):
        return self.__fr

    @fr.setter
    def fr(self, value):
        self.__fr = value

    @property
    def gm(self):
        return self.__gm

    @gm.setter
    def gm(self, value):
        self.__gm = value

    @property
    def i1(self):
        return self.__i1

    @i1.setter
    def i1(self, value):
        self.__i1 = value

    @property
    def i2(self):
        return self.__i2

    @i2.setter
    def i2(self, value):
        self.__i2 = value

    @property
    def timeFirstConnected(self):
        return self.__timeFirstConnected

    @timeFirstConnected.setter
    def timeFirstConnected(self, value):
        self.__timeFirstConnected = value

    @property
    def goalTime(self):
        return self.__goalTime

    @goalTime.setter
    def goalTime(self, value):
        self.__goalTime = value

    @property
    def timeActive(self):
        return self.__timeActive

    @timeActive.setter
    def timeActive(self, value):
        self.__timeActive = value

    @property
    def timeFinished(self):
        return self.__timeFinished

    @timeFinished.setter
    def timeFinished(self, value):
        self.__timeFinished = value
