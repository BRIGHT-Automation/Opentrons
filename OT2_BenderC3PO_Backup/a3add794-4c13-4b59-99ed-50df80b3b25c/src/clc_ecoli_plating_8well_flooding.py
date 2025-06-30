metadata = {
    'protocolName': 'CLC E. coli 8-well plate flooding_16wells',
    'fileName': 'CLC_8well_plate_flooding.py',
    'author': 'Rikke <riras@dtu.dk>',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}

import json
from opentrons import types


def run(protocol):

    well_count = 32
    plating_volume = 250
    plate_format = 8

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

    def calculate_plate(w, plate_format):
        p = w // plate_format
        return (p)

    def calculate_well(w, plate_format):
        return (w % plate_format)

    def plate(w, vol):
        p300.pick_up_tip()
        p300.mix(3, 250, coli_dw.wells()[w])
        p300.aspirate(vol, coli_dw.wells()[w])
        plate = calculate_plate(w, plate_format)
        well = calculate_well(w, plate_format)
        depth = agarPlates[plate].wells()[well].bottom(z=6)
        p300.dispense(vol, depth)
        p300.drop_tip()

    for i in range(2):
        for well in range(well_count):
            plate(well, plating_volume)
