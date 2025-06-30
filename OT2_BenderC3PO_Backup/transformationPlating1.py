metadata = {
    'protocolName': 'Coco - one drop plating 1-48',
    'fileName': 'transformationPlating1.py',
    'author': 'Jaime <jmutr@dtu.dk>, from Rikkes <riras@dtu.dk> protocol',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}


def run(protocol):

    well_count = 48
    plating_volume = 50
    plate_format = 8
    controls_on_last_row = False

    #Load Tips

    tips300 = [protocol.load_labware('opentrons_96_filtertiprack_200ul', '9')]
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

    cells_dw = protocol.load_labware("corning_96_wellplate_360ul_flat", 7)
    #water_res = protocol.load_labware("agilent_1_reservoir_290ml", 8)

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

        p300.pick_up_tip(tips300[0].wells()[src])
        #p300.aspirate(200, water_res.wells()[0])
        #p300.dispense(200, cells_dw.wells()[src])
        #p300.mix(3, plating_volume, cells_dw.wells()[src], rate=0.5)
        p300.aspirate(vol, cells_dw.wells()[src], rate=0.2)
        dest_plate = calculate_plate(dest, plate_format)
        dest_well = calculate_well(dest, plate_format)
        depth = agarPlates[dest_plate].wells()[dest_well].bottom(z=6)
        p300.dispense(vol, depth, rate=0.4)
        p300.blow_out(depth)
        p300.drop_tip()
        src += 1
        dest += 1

    for well in range(well_count):
        plate(well, plating_volume)
        
