# pylama:ignore=E501

from opentrons import instruments, robot
from opentrons.containers import load as containers_load
from opentrons.trackers import pose_tracker
from numpy import isclose


def test_pipette_models():
    robot.reset()
    p = instruments.P10_Single(mount='left')
    assert p.channels == 1
    assert p.max_volume > 10
    p = instruments.P10_Multi(mount='right')
    assert p.channels == 8
    assert p.max_volume > 10

    robot.reset()
    p = instruments.P50_Single(mount='left')
    assert p.channels == 1
    assert p.max_volume > 50
    p = instruments.P50_Multi(mount='right')
    assert p.channels == 8
    assert p.max_volume > 50

    robot.reset()
    p = instruments.P300_Single(mount='left')
    assert p.channels == 1
    assert p.max_volume > 300
    p = instruments.P300_Multi(mount='right')
    assert p.channels == 8
    assert p.max_volume > 300

    robot.reset()
    p = instruments.P1000_Single(mount='left')
    assert p.channels == 1
    assert p.max_volume > 1000


def test_pipette_max_deck_height():
    robot.reset()
    tallest_point = robot._driver.homed_position['Z']
    p = instruments.P300_Single(mount='left')
    assert p._max_deck_height() == tallest_point

    for tip_length in [10, 25, 55, 100]:
        p._add_tip(length=tip_length)
        assert p._max_deck_height() == tallest_point - tip_length
        p._remove_tip(length=tip_length)


def test_retract():
    robot.reset()
    plate = containers_load(robot, '96-flat', '1')
    p300 = instruments.P300_Single(mount='left')
    from opentrons.drivers.smoothie_drivers.driver_3_0 import HOMED_POSITION

    p300.move_to(plate[0].top())

    assert p300.previous_placeable == plate[0]
    current_pos = pose_tracker.absolute(
        robot.poses,
        p300)
    assert current_pos[2] == plate[0].top()[1][2]

    p300.retract()

    assert p300.previous_placeable is None
    current_pos = pose_tracker.absolute(
        robot.poses,
        p300.instrument_mover)
    assert current_pos[2] == HOMED_POSITION['A']


def test_aspirate_move_to():
    robot.reset()
    tip_rack = containers_load(robot, 'tiprack-200ul', '3')
    p300 = instruments.P300_Single(
        mount='left', tip_racks=[tip_rack])
    p300.pick_up_tip()

    x, y, z = (161.0, 116.7, 0.0)
    plate = containers_load(robot, '96-flat', '1')
    well = plate[0]
    pos = well.from_center(x=0, y=0, z=-1, reference=plate)
    location = (plate, pos)

    robot.poses = p300._move(robot.poses, x=x, y=y, z=z)
    robot.calibrate_container_with_instrument(plate, p300, False)

    p300.aspirate(100, location)
    current_pos = pose_tracker.absolute(
        robot.poses,
        p300.instrument_actuator)
    assert (current_pos == (8.402, 0.0, 0.0)).all()

    current_pos = pose_tracker.absolute(robot.poses, p300)
    assert isclose(current_pos, (175.34,  127.94,   10.5)).all()


def test_dispense_move_to():
    robot.reset()
    tip_rack = containers_load(robot, 'tiprack-200ul', '3')
    p300 = instruments.P300_Single(
                   mount='left',
                   tip_racks=[tip_rack])

    x, y, z = (161.0, 116.7, 0.0)
    plate = containers_load(robot, '96-flat', '1')
    well = plate[0]
    pos = well.from_center(x=0, y=0, z=-1, reference=plate)
    location = (plate, pos)

    robot.poses = p300._move(robot.poses, x=x, y=y, z=z)
    robot.calibrate_container_with_instrument(plate, p300, False)

    p300.pick_up_tip()
    p300.aspirate(100, location)
    p300.dispense(100, location)
    current_pos = pose_tracker.absolute(
        robot.poses,
        p300.instrument_actuator)
    assert (current_pos == (3.0, 0.0, 0.0)).all()

    current_pos = pose_tracker.absolute(robot.poses, p300)
    assert isclose(current_pos, (175.34,  127.94,   10.5)).all()


def test_delay_calls(monkeypatch):
    from opentrons import robot
    from opentrons.instruments import pipette
    robot.reset()
    p300 = instruments.P300_Single(mount='right')

    cmd = []

    def mock_pause():
        nonlocal cmd
        cmd.append('pause')

    def mock_resume():
        nonlocal cmd
        cmd.append('resume')

    def mock_sleep(seconds):
        cmd.append("sleep {}".format(seconds))

    monkeypatch.setattr(robot, 'pause', mock_pause)
    monkeypatch.setattr(robot, 'resume', mock_resume)
    monkeypatch.setattr(pipette, '_sleep', mock_sleep)

    p300.delay(seconds=4, minutes=1)

    assert 'pause' in cmd
    assert 'sleep 64.0' in cmd
    assert 'resume' in cmd
