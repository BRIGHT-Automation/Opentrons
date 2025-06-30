#This protocol takes 
#   6 x 384 well plates from greiner
#   a 1 well container with pbs 1x freshly boil

#Run time for 6 plates : around 50 min, ie 8.3 min/plate
#        
# Requires 1x 300 µL Tip racks 

from opentrons import protocol_api

metadata = {
    'protocolName': 'isolation_restreaking_plate_prep',
    'author': 'Jeremy Armetta',
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    # Load a P300 multi on the left slot
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    p300Multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tips300])

    
    locs = [1]
    plates = [protocol.load_labware("corning_96_wellplate_360ul_flat", slot,)
    				for slot in locs]

    wells = [0,8]
    
    p300Multi.flow_rate.dispense = 200

    def transfer_plate(w, plate):
        p300Multi.flow_rate.aspirate = 150
        p300Multi.aspirate(95,plate.wells()[w])
        p300Multi.dispense(95,plate.wells()[w+16])

    
    for plate in plates:
    	p300Multi.pick_up_tip()
    	for well in wells:
            transfer_plate(well, plate)
    	p300Multi.drop_tip()
      
    protocol.comment('Run completed')