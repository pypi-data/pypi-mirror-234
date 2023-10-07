from vlcsim.receiver import *
import pytest


class TestReceiver:
    @pytest.fixture(autouse=True)
    def reset(self):
        yield
        Receiver.receiversCreated = 0

    def testConstructor(self):
        receiver = Receiver(-1.989796, -1.989796, 0, 1e-4, 1.0, 1.5, 70.0)

    def testGetters(self):
        receiver1 = Receiver(-1.989796, -1.989796, 0, 1e-4, 1.0, 1.5, 70.0)
        receiver2 = Receiver(-1.989796, -1.989796, 0, 1e-4, 1.0, 1.5, 70.0)

        assert receiver1.ID == 0
        assert receiver2.ID == 1
        assert Receiver.receiversCreated == 2

        assert receiver1.x == -1.989796
        assert receiver1.y == -1.989796
        assert receiver1.z == 0
        assert receiver1.aDet == 1e-4
        assert receiver1.ts == 1.0
        assert receiver1.index == 1.5
        assert receiver1.fov == 70
        assert receiver1.gCon == pytest.approx(2.5480672457215374)
