nmols = {'A1': 25.84, 'A2': 26.32, 'A3': 28.23, 'A4': 29.08, 'A5': 25.64, 'A6': 28.65, 'B1': 26.49, 'B2': 26.79, 'B3': 24.94, 'B4': 28.17, 'B5': 26.46, 'B6': 27.42, 'C1': 28.44, 'C2': 28.67, 'C3': 29, 'C4': 31.29, 'C5': 28.5, 'C6': 29.33, 'D1': 30.11, 'D2': 26.74, 'D3': 26.78, 'D4': 24.97, 'D5': 19.93, 'D6': 32.06, 'E1': 25.54, 'E2': 28.85, 'E3': 34.95, 'E4': 24.83, 'E5': 34.95, 'E6': 27.16, 'F1': 31.76, 'F2': 27.27, 'F3': 22.3, 'F4': 29.58, 'F5': 22.55, 'G1': 28.64, 'G2': 23.61, 'G3': 21.38, 'G4': 26.01, 'G5': 25.75, 'H1': 24.32, 'H2': 23.88, 'H3': 21.91, 'H4': 36.04, 'H5': 25.08}	


metadata = {
    'protocolName': 'AAdd water and Dilute Oligos_FIX',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'DTU Biosustain',
    'apiLevel': '2.9'
}

def run(protocol):
    tips1000 = [protocol.load_labware("geb_96_tiprack_1000ul", 1)]
    tips20 = [protocol.load_labware("opentrons_96_filtertiprack_20ul", 3)]
    p1000 = protocol.load_instrument('p1000_single', 'right', tip_racks=tips1000)
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks = tips20)
    
    oligo_plate = protocol.load_labware("nest_96_wellplate_2ml_deep", 2)
    rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", 4)
    dilutionPlate = protocol.load_labware("gp_plate_96", 5)
    echoPlate = protocol.load_labware("echo_384_pp_standard", 6)
    water = rack["A1"]
    

    p1000.distribute(90, water, [dilutionPlate.wells_by_name()[w] for w in nmols.keys()])

    for k in list(nmols.keys())[27:]:
        p1000.transfer(nmols[k]*10, 
                      water, 
                      oligo_plate[k], 
                       mix_after = (5, 800))

    
    i = 0
    for i in range(len(nmols.keys())):
      p20.pick_up_tip()
      p20.transfer(10, oligo_plate.wells()[i], dilutionPlate.wells()[i], mix_after=(5, 20), new_tip = "never")
      for x in range(3):
        p20.transfer(20, dilutionPlate.wells()[i], echoPlate.wells()[i], new_tip = "never")
      i+=1
      p20.drop_tip()
    
