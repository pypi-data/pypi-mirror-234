from vlcsim.vled import *
import pytest


class TestVLed:
    @pytest.fixture(autouse=True)
    def reset(self):
        VLed.numberOfVLeds = 0

    def testConstructor(self):
        vled = VLed(-1.25, -1.25, 2.15, 60, 60, 20, 70)

    def testGetters(self):
        vled = VLed(-1.25, -1.25, 2.15, 60, 60, 20, 70)
        vled2 = VLed(-1.25, -1.25, 2.15, 60, 60, 20, 70)

        assert vled.ID == 0
        assert vled2.ID == 1
        assert VLed.numberOfVLeds == 2

        assert vled.x == -1.25
        assert vled.y == -1.25
        assert vled.z == 2.15
        assert vled.nLedsX == 60
        assert vled.nLedsY == 60
        assert vled.ledPower == 20
        assert vled.theta == 70
        assert vled.numberOfLeds == 3600
        assert vled.ml == pytest.approx(0.6460587703487339)
