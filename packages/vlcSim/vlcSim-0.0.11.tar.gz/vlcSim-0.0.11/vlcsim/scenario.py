from .vled import *
from .receiver import *
from .rf import RF


class Scenario:
    numberOfAPs = 0

    def __init__(
        self, width: float, length: float, height: float, nGrids: int, rho: float
    ) -> None:
        self.__length = length  # x
        self.__width = width  # y
        self.__height = height  # z

        self.__rho = rho

        self.__start_x = -self.__width / 2
        self.__start_y = -self.__length / 2
        self.__end_x = self.__width / 2
        self.__end_y = self.__length / 2

        self.__mobile_terminals = []
        self.__vleds = []
        self.__femtocells = []

        self.__vledsPositions = []
        self.__rfsPositions = []

        self.__nx = round(self.__length * nGrids)
        self.__ny = round(self.__width * nGrids)
        self.__nz = round(self.__height * nGrids)

        self.__g_x = np.linspace(self.__start_x, self.__end_x, self.__nx)
        self.__g_y = np.linspace(self.__start_y, self.__end_y, self.__ny)
        self.__g_z = np.linspace(0, self.__height, self.__nz)

        self.__g_xyz = np.array([self.__g_x, self.__g_y, self.__g_z], dtype=object)

    def addVLed(self, vled: VLed):
        self.__vleds.append(vled)
        self.__vledsPositions.append(Scenario.numberOfAPs)
        Scenario.numberOfAPs += 1

    def addRF(self, rf: RF):
        self.__femtocells.append(rf)
        self.__rfsPositions.append(Scenario.numberOfAPs)
        Scenario.numberOfAPs += 1

    def getPowerInPointFromWalls(self, receiver: Receiver, vledID: int) -> float:
        vled = self.__vleds[vledID]
        h1 = self.__channelGainWall(receiver, vled, 1, 0)
        h2 = self.__channelGainWall(receiver, vled, 0, 1)
        h3 = self.__channelGainWall(receiver, vled, 1, 2)
        h4 = self.__channelGainWall(receiver, vled, 0, 3)
        power = (h1 + h2 + h3 + h4) * vled.totalPower * receiver.ts * receiver.gCon
        return float(power)

    def getPowerInPointFromVled(self, receiver: Receiver, vledID: int) -> float:
        vled = self.__vleds[vledID]
        D_los = m.sqrt(
            (receiver.x - vled.x) ** 2
            + (receiver.y - vled.y) ** 2
            + (receiver.z - vled.z) ** 2
        )
        cosphi = (vled.z - receiver.z) / D_los
        # print(vled.x, vled.y, vled.z)
        # print(receiver.x, receiver.y, receiver.z)
        # print(cosphi)
        r_angle = m.degrees(m.acos(cosphi))
        H = (
            (vled.ml + 1)
            * receiver.aDet
            * cosphi ** (vled.ml + 1)
            / (2 * m.pi * D_los**2)
        )
        power = (
            vled.totalPower * H * receiver.ts * receiver.gCon
            if abs(r_angle) <= receiver.fov
            else 0
        )
        return power

    def __channelGainWall(self, receiver: Receiver, vled, posVar, posFixed) -> float:
        wall = None
        dA = self.__height
        if posFixed == 0:
            wall = (self.__start_x, 0)
            dA *= self.__length / (self.__nx * self.__nz)
        elif posFixed == 1:
            wall = (self.__start_y, 1)
            dA *= self.__width / (self.__ny * self.__nz)
        elif posFixed == 2:
            wall = (self.__end_x, 0)
            dA *= self.__length / (self.__nx * self.__nz)
        elif posFixed == 3:
            wall = (self.__end_y, 1)
            dA *= self.__width / (self.__ny * self.__nz)

        h = 0
        wp = np.full(3, wall[0])
        g = self.__g_xyz[posVar]
        for i in g:
            wp[posVar] = i
            for j in self.__g_z:
                wp[2] = j
                D1 = m.sqrt(np.dot(vled.position - wp, vled.position - wp))
                cosphi = abs(wp[2] - vled.position[2]) / D1
                cosalpha = abs(vled.position[wall[1]] - wp[wall[1]]) / D1
                D2 = m.sqrt(np.dot(wp - receiver.position, wp - receiver.position))
                cosbeta = abs(wp[wall[1]] - receiver.position[wall[1]]) / D2
                cospsi = abs(wp[2] - receiver.position[2]) / D2
                if abs(m.degrees(m.acos(cospsi))) <= receiver.fov:
                    h = h + (vled.ml + 1) * receiver.aDet * self.__rho * dA * (
                        cosphi**vled.ml
                    ) * cosalpha * cosbeta * cospsi / (
                        2 * (m.pi**2) * (D1**2) * (D2**2)
                    )
        return h

    @property
    def numberOfVLeds(self):
        return len(self.__vleds)

    @property
    def numberOfRFs(self):
        return len(self.__femtocells)

    @property
    def vleds(self):
        return self.__vleds

    @property
    def rfs(self):
        return self.__femtocells

    @property
    def start_x(self):
        return self.__start_x

    @start_x.setter
    def start_x(self, value):
        self.__start_x = value

    @property
    def start_y(self):
        return self.__start_y

    @start_y.setter
    def start_y(self, value):
        self.__start_y = value

    @property
    def end_x(self):
        return self.__end_x

    @end_x.setter
    def end_x(self, value):
        self.__end_x = value

    @property
    def end_y(self):
        return self.__end_y

    @end_y.setter
    def end_y(self, value):
        self.__end_y = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def vledsPositions(self):
        return self.__vledsPositions

    @property
    def rfsPositions(self):
        return self.__rfsPositions

    def snrVled(self, receiver: Receiver, vled: VLed) -> float:
        powerReceived = self.getPowerInPointFromVled(
            receiver, vled.ID
        ) + self.getPowerInPointFromWalls(receiver, vled.ID)
        rd = (2 * receiver.q * receiver.s * powerReceived * receiver.b) + (
            2 * receiver.q * receiver.ibg * receiver.i1 * receiver.b
        )
        rt = (
            8
            * m.pi
            * receiver.cb
            * receiver.tk
            * receiver.n
            * receiver.a
            * receiver.b**2
            * (
                (receiver.i1 / receiver.gv)
                + (2 * m.pi)
                * receiver.fr
                / receiver.gm
                * receiver.n
                * receiver.a
                * receiver.i2
                * receiver.b
            )
        )
        rg = rd + rt
        return (receiver.s * powerReceived) ** 2 / rg

    def snrRf(self, receiver: Receiver, rf: RF) -> float:
        df = m.sqrt(
            (receiver.x - rf.x) ** 2
            + (receiver.y - rf.y) ** 2
            + (receiver.z - rf.z) ** 2
        )

        return rf.pf * rf.Af * df ** (-rf.Ef)
