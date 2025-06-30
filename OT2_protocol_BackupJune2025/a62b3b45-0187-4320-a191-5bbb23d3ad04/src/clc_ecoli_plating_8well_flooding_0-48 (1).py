metadata = {
    'protocolName': 'CLC E. coli 8-well plate flooding_0-48_48wells',
    'fileName': 'clc_ecoli_plating_8well_flooding_0-48.py',
    'author': 'Rikke <riras@dtu.dk>',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}


def run(protocol):
    import math

    well_count = 48
    plating_volume = 420
    plate_format = 8
    controls_on_last_row = False
    

    #Load Tips

    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '10')]
    p300 = protocol.load_instrument("p300_single", "right", tip_racks=tips300)
    max_tip_volume = 250

    # Define the p20 pipette even though it's not being used, just so the instrument knows it's there
    #tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '11')]
    #p20 = protocol.load_instrument("p300_8-Channel GEN2", "left", tip_racks=tips20)

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
        
        src = w
        dest = w
        if (w + 1) % 24 == 0 and controls_on_last_row == True:
            dest = dest + 1
        dest_plate = calculate_plate(dest, plate_format)
        dest_well = calculate_well(dest, plate_format)
        depth = agarPlates[dest_plate].wells()[dest_well].bottom(z=10)

        num_loops = math.ceil(vol / max_tip_volume)
        tip_volume = math.ceil(vol / num_loops)

        p300.pick_up_tip(tips300[0].wells()[src])
        p300.mix(5, tip_volume, coli_dw.wells()[src])
        for i in range(num_loops):
            p300.aspirate(tip_volume, coli_dw.wells()[src])
            p300.dispense(tip_volume, depth)
        p300.drop_tip()
        src += 1
        dest += 1

    for well in range(well_count):
        plate(well, plating_volume)
    
