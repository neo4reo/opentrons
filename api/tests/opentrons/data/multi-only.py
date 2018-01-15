from opentrons import containers, instruments

tiprack = containers.load('tiprack-200ul', 'B3')
trough = containers.load('trough-12row', 'C3')
trash = containers.load('trash-box', 'C4')
plate = containers.load('96-flat', 'B2')

multi = instruments.Pipette(
    mount='left',
    max_volume=300,
    min_volume=10,
    name="p200S",
    tip_racks=[tiprack],
    trash_container=trash,
    channels=8)

for tips in [tiprack.rows(0), tiprack.rows[-1]]:
    multi.pick_up_tip(tips)
    multi.aspirate(100, trough.rows[0])
    multi.aspirate(100, trough.rows[-1])

    multi.dispense(100, plate.rows[0])
    multi.dispense(100, plate.rows[-1])
    multi.drop_tip(tips)