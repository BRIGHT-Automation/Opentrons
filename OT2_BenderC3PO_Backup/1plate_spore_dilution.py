import opentrons
from opentrons import protocol_api

metadata = metadata = {'apilevel' : '2.16',
            'protocolName': 'Serial Dilution Bioassay', 
            ' ' : ' '}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}


# oki, so the overall protocol will be: 
# do manually the dilutions in falcons and pour them into a 12 well reservoir
# from this reservoir, I think what they want to do is a serial dilution in 10 96-well cryoplates
# and from these cryoplates, the SOP says to 'stamp' in PDA plates
# i guess we'll just take a small volume

# but i don't really get why would we make 10 plates and stamp those 10 plates in another 10 PDA plates
# as in okay, we have 10 plates, more variability and storage but
# isnt it better to just make 1 cryplate and then 'stamp' it in 10 PDA plates?
# im gonna do the latter, if we end up doing 10 (we cannot in opentron un 1 run) ill just modify it

def run(protocol: protocol_api.ProtocolContext):
    # lets load the labware
    tips = protocol.load_labware('opentrons_96_tiprack_300uL', 11) # idk if the names are that ones
    reservoir = protocol.load_labware('nest_12_reservoir_15mL', 10) 
    plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 1)            
    pipette = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tips])

    # also, this protocol uses transfer, which discard the tip everytime is used. 
    # if the serial dilution is positioned in a specific way (from more to less diluted)
    # we could use the same set of tips and we save plastic!

    # now the actual protocol

    pipette.pick_up_tip()
    for i in range(12): # 12 columns
        source_well = reservoir.wells()[i]
        dest_wells = plate.columns()[i]

        pipette.transfer(100, source_well, dest_wells, new_tip='never') # volume of 100uL as that was the aprox volume when making the batch spores
        pipette.mix(2, 50, dest_wells[0])

    pipette.drop_tip()
    