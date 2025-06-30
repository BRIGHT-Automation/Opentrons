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

    
    p300Multi.flow_rate.dispense = 200

    for plate in plates:
    	p300Multi.pick_up_tip()
    	p300Multi.transfer(100,plate.wells_by_name()['A1'],plate.wells_by_name()['A3'], new_tip='never')
    	p300Multi.transfer(100,plate.wells_by_name()['A2'],plate.wells_by_name()['A4'], new_tip='never')
    	p300Multi.drop_tip()
      
    protocol.comment('Run completed')