import pytest
from unittest.mock import MagicMock
from uav_control import UAVControl


@pytest.fixture
def mock_uav_control():
    uav_control = UAVControl("udp:127.0.0.1:14551")
    uav_control.master = MagicMock()
    return uav_control


def test_arm(mock_uav_control):
    mock_uav_control.master.arducopter_arm = MagicMock()
    mock_uav_control.arm()
    mock_uav_control.master.arducopter_arm.assert_called_once()


def test_takeoff(mock_uav_control):
    mock_uav_control.master.recv_match.return_value = MagicMock(lat=0, lon=0)
    mock_uav_control.takeoff(100)
    mock_uav_control.master.mav.command_long_send.assert_called_once()


def test_get_telemetry(mock_uav_control):
    mock_uav_control.master.recv_match.return_value = MagicMock(get_type=MagicMock(return_value="VFR_HUD"), airspeed=10)
    telemetry = mock_uav_control.get_telemetry()
    assert telemetry is not None
    assert telemetry['airspeed'] == 10


def test_invalid_takeoff(mock_uav_control):
    with pytest.raises(ValueError):
        mock_uav_control.takeoff(-100)


def test_set_mode(mock_uav_control):
    mock_uav_control.set_mode("GUIDED")
    mock_uav_control.master.set_mode.assert_called_once()
