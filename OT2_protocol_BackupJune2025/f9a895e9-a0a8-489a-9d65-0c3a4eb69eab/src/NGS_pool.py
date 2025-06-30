from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'Pooling Columns from 96-Well Plate',
    'author': 'Your Name',
    'description': 'Pools the first 4 columns of a 96-well plate in one trough, the next 4 in another trough, and the last 4 in a 3rd trough using a multi-channel pipette.',
    'apiLevel': '2.10'
}

# Protocol function
def run(protocol: protocol_api.ProtocolContext):

    # Labware
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    temp_mod_1 = protocol.load_module(module_name='temperature module',location=10)
    working_plate = temp_mod_1.load_labware(name='opentrons_96_aluminumblock_nest_wellplate_100ul')
    trough = protocol.load_labware('nest_12_reservoir_15ml', '11')


    # Pipettes
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1])

    # Air gap volume
    air_gap_vol = 20

    # Pooling first 4 columns
    p300_multi.pick_up_tip()
    for col in range(3):
        p300_multi.aspirate(50, working_plate.columns()[col][0].bottom(z=1))
    p300_multi.aspirate(50, working_plate.columns()[3][0].bottom(z=1))
    p300_multi.air_gap(air_gap_vol)
    p300_multi.dispense(250 + air_gap_vol, trough['A10'].bottom())
    p300_multi.drop_tip()

    # Pooling next 4 columns
    p300_multi.pick_up_tip()
    for col in range(4, 7):
        p300_multi.aspirate(50, working_plate.columns()[col][0].bottom(z=1))
    p300_multi.aspirate(50, working_plate.columns()[7][0].bottom(z=1))
    p300_multi.air_gap(air_gap_vol)
    p300_multi.dispense(250 + air_gap_vol, trough['A11'].bottom())
    p300_multi.drop_tip()

    # Pooling last 4 columns
    p300_multi.pick_up_tip()
    for col in range(8, 11):
        p300_multi.aspirate(50, working_plate.columns()[col][0].bottom(z=1))
    p300_multi.aspirate(50, working_plate.columns()[11][0].bottom(z=1))
    p300_multi.air_gap(air_gap_vol)
    p300_multi.dispense(250 + air_gap_vol, trough['A12'].bottom())
    p300_multi.drop_tip()