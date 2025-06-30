import opentrons
from opentrons import protocol_api

metadata = {'apilevel' : '2.16',
            'protocolName': 'Coco - 96 deep-well plates inoculation',
            'author': 'Jaime <jmutr@dtu.dk>'}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}


def run(protocol: protocol_api.ProtocolContext):
    tips = [
    protocol.load_labware('opentrons_96_tiprack_300uL', slot)
    for slot in range(1, 4)]
    reservoir = protocol.load_labware('nest_1_reservoir_195ml', 11)
    dw_plates = [
    protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', slot)
    for slot in range(7, 10)]
    precul_plates = [
    protocol.load_labware('corning_96_wellplate_360ul_flat', slot)
    for slot in range(4, 7)]

    pip = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=tips)
    
    # first we fill the wells with media
    pip.pick_up_tip()
    for plate in dw_plates:
        pip.distribute(300, reservoir['A1'], plate.rows()[0], new_tip='never')
    pip.return_tip()
    
    # then we inoculate
    for i in range(3):
        precol = precul_plates[i].columns()
        dwcol = dw_plates[i].columns()
        tip = tips[i].wells()
        for j in range(12):
            pip.pick_up_tip(tip[j])
            pip.transfer(50, precol[j][0], dwcol[j][0], mix_after=(2,50), new_tip='never')
            pip.drop_tip(tip[j])