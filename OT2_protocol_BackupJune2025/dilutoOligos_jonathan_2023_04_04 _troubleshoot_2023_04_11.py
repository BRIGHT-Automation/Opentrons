nmoles = {
    'D5': 58.65,
    'D6': 91.29,
    'D7': 58.36,
    'E1': 74.55,
    'E2': 67.9,
    'E3': 84.02,
    'E4': 76.72,
    'E5': 76.22,
    'E6': 57.23,
    'E7': 70.8,
    'F1': 81.19,
    'F2': 57.55,
    'F3': 67.37,
    'F4': 53,
    'F5': 80.4,
    'F6': 65.99,
    'F7': 77.92,
    'G1': 82.56,
    'G2': 85.41,
    'G3': 72.03,
    'G4': 77.01,
    'G5': 58.25,
    'G6': 66.57,
    'G7': 84.97,
    'H1': 58.51,
    'H2': 85.11,
    'H3': 74.62,
    'H4': 70.17,
    'H5': 88.92,
    'H6': 61.86,
    'H7': 80.41
}

#'A1': 80.8 removed
#'A2': 79.28 removed
#'A3': 61.25,
#   'A4': 80.88,
#    'A5': 83.32,
#   'A6': 81.75,
#  'A7': 52.01,
# 'B1': 52.38,
#'B2': 80.2,
#'B3': 60.18,
#'B4': 53.4,
#'B5': 51.44,
#'B6': 65.34,
#'B7': 70.21,
#'C1': 63.22,
#'C2': 77.28,
#'C3': 74.14,
#'C4': 67.72,
#'C5': 77.87,
#'C6': 45.12,
#'C7': 84.99,
#'D1': 65.83,
#'D2': 66.17,
#'D3': 69.75,
#'D4': 86.59,

metadata = {
    'protocolName':
    'Add water and Dilute Oligos jonathan 2023.04.04_troubledshooted2023-04-11',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'DTU Biosustain',
    'apiLevel': '2.9'
}


def run(protocol):
    tips1000 = [protocol.load_labware("geb_96_tiprack_1000ul", 1)]
    tips20 = [protocol.load_labware("opentrons_96_filtertiprack_20ul", 3)]
    p1000 = protocol.load_instrument('p1000_single',
                                     'right',
                                     tip_racks=tips1000)
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips20)

    oligo_plate = protocol.load_labware(
        "idt_vbot_96", 2)  #abgenestorage_96_wellplate_1200ul normally
    water_rack = protocol.load_labware(
        "opentrons_6_tuberack_falcon_50ml_conical", 4)
    water = water_rack["A1"]
    dilutionPlate = protocol.load_labware("gp_plate_96", 5)
    echoPlate = protocol.load_labware("echo_384_pp_standard",
                                      6)  # echo_384_pp_standard
    deepwell = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep",
                                     7)

    #prefill dilution plate with 90µL water in relevant wells
    #p1000.distribute(90, water, [dilutionPlate[well] for well in nmoles.keys()]) #how to not put tip back?? trash=F alse still tells system tip is dirty in rack
    '''
    for well in nmoles.keys():
        #define stock volume for given well
        final_stock_volume = nmoles[well] * 10

        p1000.pick_up_tip()
        #prefill oligo stock deepwell with water minus the 350µL volume added later
        p1000.transfer(final_stock_volume - 350,
                       water.bottom(z=8),
                       deepwell[well],
                       new_tip="never")

        #transfer 350µL water to the oligo plate and mix
        p1000.transfer(350, water.bottom(z=8), oligo_plate[well], new_tip="never")
        for mix in range(15):
            p1000.aspirate(300, oligo_plate[well], rate=6)
            p1000.dispense(300, oligo_plate[well].bottom(z=7), rate=6)
            p1000.aspirate(300, oligo_plate[well], rate=6)
            p1000.dispense(300, oligo_plate[well].bottom(z=2), rate=6)

        #transfer the 350µL oligo suspension to the deepwell and mix
        p1000.transfer(350, oligo_plate[well], deepwell[well], new_tip="never")
        for mix in range(6):
            p1000.aspirate(final_stock_volume-50, deepwell[well].bottom(z=2), rate=6)
            p1000.dispense(final_stock_volume-50,
                           deepwell[well].bottom(z=15),
                           rate=6)
        p1000.aspirate(final_stock_volume-50, deepwell[well].bottom(z=2), rate=6)
        p1000.dispense(final_stock_volume-50, deepwell[well].bottom(z=2), rate=6)

        for get_all_dna_left in range(2):
            p1000.transfer(350,
                           deepwell[well],
                           oligo_plate[well],
                           new_tip="never")
            for mix in range(2):
                p1000.aspirate(350, oligo_plate[well], rate=6)
                p1000.dispense(350, oligo_plate[well].bottom(z=7), rate=6)
            p1000.transfer(350,
                           oligo_plate[well],
                           deepwell[well],
                           new_tip="never")
            for mix in range(2):
                p1000.aspirate(final_stock_volume, deepwell[well].bottom(z=2), rate=6)
                p1000.dispense(final_stock_volume,
                               deepwell[well].bottom(z=15),
                               rate=6)

        p1000.drop_tip()
    '''
    '''
    #Mix 10uL oligo stock with the 90µL prefilled water in the dilution plate = 10x dilution
    for well in nmoles.keys():
        p20.pick_up_tip()
        p20.transfer(10, oligo_plate[well], dilutionPlate[well], new_tip="never")
        
        #Mixing with different disp vs asp distance and high flow rate
        for mix in range(5):
            p20.aspirate(20, dilutionPlate[well], rate=6)
            p20.dispense(20, dilutionPlate[well].bottom(z=6), rate=6)
        p20.aspirate(20, dilutionPlate[well], rate=6)
        p20.dispense(20, dilutionPlate[well].bottom(z=2), rate=6)
        
	
        #transfer 3x20µL of dilution plate to the echo 384 plate
        for i in range(3):
            p20.transfer(20, dilutionPlate[well], echoPlate[well], new_tip="never")
        p20.drop_tip()
     '''
    p1000.distribute(
        180, water,
        [dilutionPlate.wells()[i] for i in range(2,
                                                 len(nmoles) + 25)])

    for i in range(2, len(nmoles) + 25):
        p20.pick_up_tip()
        p20.transfer(20,
                     deepwell.wells()[i],
                     dilutionPlate.wells()[i],
                     new_tip="never")

        #Mixing with different disp vs asp distance and high flow rate
        for mix in range(6):
            p20.aspirate(20, dilutionPlate.wells()[i], rate=6)
            p20.dispense(20, dilutionPlate.wells()[i].bottom(z=6), rate=6)
        p20.aspirate(20, dilutionPlate.wells()[i], rate=6)
        p20.dispense(20, dilutionPlate.wells()[i].bottom(z=2), rate=6)

        for transfers in range(3):
            p20.transfer(20,
                         dilutionPlate.wells()[i],
                         echoPlate.wells()[i],
                         new_tip="never")
        p20.drop_tip()
