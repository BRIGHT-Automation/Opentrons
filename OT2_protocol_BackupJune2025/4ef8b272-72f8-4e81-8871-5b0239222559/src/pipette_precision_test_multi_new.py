from opentrons import protocol_api

metadata = {
    'protocolName': 'Pipette precision test for p300_multi',
    'author': 'Name <tgrra@biosustain.dtu.dk>',
    'description': 'a simple script to measure the weight of water to calculate accuracy and precision using bromophenol blue or phenol red',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    
    # Define labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    deepwell_plate_water = protocol.load_labware('nest_96_wellplate_2ml_deep', 1)
    deepwell_plate_dye = protocol.load_labware('nest_96_wellplate_2ml_deep', 3)
    tipracks =[protocol.load_labware('opentrons_96_tiprack_300ul', slot) for slot in [4,5]]
    
    # Define pipette
    pipette = protocol.load_instrument('p300_multi', 'left', tip_racks = tipracks)
    
    # Define concentrations for each column
    concentrations = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.0]
    total_volume = 200  # uL per well
    
    # First, add the correct amount of MilliQ water to each well
    for col, conc in enumerate(concentrations):
        water_source = deepwell_plate_water.columns()[col]
        water_vol = total_volume if conc == 0 else total_volume * (1 - (conc / 0.1))
        pipette.transfer(water_vol, water_source, plate.columns()[col])

    
    # Then, add the correct amount of dye to each well
    for col, conc in enumerate(concentrations):
        if conc > 0:
            dye_source = deepwell_plate_dye.columns()[col]
            dye_vol = total_volume * (conc / 0.1)
            pipette.transfer(dye_vol, dye_source, plate.columns()[col], mix_after=(2, 100))