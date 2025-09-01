metadata = {
    'protocolName': 'CLC Conjugation 8-well plate flooding_0-48_48wells',
    'fileName': 'CLC_8well_plate_flooding.py',
    'author': 'Rikke <riras@dtu.dk> - modified Lachlan',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}

import json
from opentrons import types


def run(protocol):

    well_count = 48
    plating_volume = 250

    #Load Tips

    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '10')]
    p300 = protocol.load_instrument("p300_single", "right", tip_racks=tips300)

    # Define the p20 pipette even though it's not being used, just so the instrument knows it's there
    #tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '11')]
    #p20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=tips20)

    #Load plates
    plate_type = "thermoscientificnunc_8_wellplate_12000ul"
    locs = [1, 2, 3, 4, 5, 6]
    agarPlates = [
        protocol.load_labware(plate_type, slot, label="Agar Plates")
        for slot in locs
    ]

    coli_dw = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 9)
    rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", 8)
    strepto = rack["A1"]

    def calculate_plate(w):
        p = w // 6
        return (p)

    def calculate_well(w):
        return (w % 6)


    def plate(w, vol):

        plate = calculate_plate(w)
        well = calculate_well(w)
        p300.pick_up_tip()

        p300.aspirate(300, strepto)
        p300.dispense(300, coli_dw.wells()[w])
        
        p300.mix(3, 250, coli_dw.wells()[w])


        depth = agarPlates[plate].wells()[well].bottom(z=6)
        for i in range(2):
            p300.aspirate(vol, coli_dw.wells()[w])
            p300.dispense(vol, depth)

        p300.drop_tip()

    for well in range(well_count):
        plate(well, plating_volume)
