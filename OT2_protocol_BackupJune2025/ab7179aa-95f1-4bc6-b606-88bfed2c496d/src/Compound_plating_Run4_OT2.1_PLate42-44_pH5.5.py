
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 23:03:18 2022

@author: AnneWeiss

whenever you target a well in row A of a plate with an 
8-channel pipette, 
it will move its topmost tip to row A, lining itself up over the entire column.
Thus,instead of targeting every well on the plate, 
you should only target the top row:
=!! Remember that row 1 is 0 in python!!!
make two compound plates as the run is in parallel
"""


# print("This is Run 1 on OT2.0")
# input("Plate 1 on Slot 5 and press Enter")
# input("Plate 5 on Slot 6 and press Enter")
# input("Plate 9 on Slot 7 and press Enter")
# input("Plate 13 on Slot 8 and press Enter")
# input("Plate 17 on Slot 9 and press Enter")
# input("Plate 21 on Slot 10 and press Enter")
# input("Plate 25 on Slot 11 and press Enter")
# input("Compound Source Plate 001 on Slot 4 and press Enter")

metadata = {'Run': 'OT2.0_Run1',
            'apiLevel': '2.15',
            'Author' : 'Anne Weiss'}



def run(protocol):
    #labware (tiprack has to be before pipette)
    #The reservoir doesnt have any columns but still use A1##; 
    #media = MHB broth II
    reservoir_media = protocol.load_labware('agilent_1_reservoir_290ml', 1) 
    
    
    source_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 4)
        
    tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul',3)
    
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', 
                                    tip_racks=[tiprack_300])
    #There are no multi1000"
    p20 = protocol.load_instrument('p20_multi_gen2', 'right',
                                   tip_racks=[tiprack_20])
    
    plate_slot5 = protocol.load_labware('corning_96_wellplate_360ul_flat', 5) 
    plate_slot6 = protocol.load_labware('corning_96_wellplate_360ul_flat', 6)
    plate_slot7 = protocol.load_labware('corning_96_wellplate_360ul_flat', 7)

    Dest_plates = (plate_slot5, plate_slot6, plate_slot7, 
                   )
  

#-------------Distribute diluent on all Destination plates

    p300.pick_up_tip()  
    for plate in Dest_plates:
        p300.transfer(90, reservoir_media['A1'], plate.columns()[:1], 
                     new_tip = "never")
        target_columns = [f'A{i}' for i in range(2, 12)]
        p300.distribute(50, reservoir_media['A1'], [plate.wells_by_name()[col] for col in target_columns], new_tip="never")
    p300.drop_tip()
    

###compound transfer
#------Transfer compounds to first column of destination plate for each plate 
#Plate on spot 5 needs column 1
    p20.pick_up_tip()
    p20.transfer(10, source_plate.columns()[1], plate_slot5.columns()[0], 
                 mix_before=(8,20),mix_after=(5,20), 
                 new_tip = "never") #transfer from cmpd plate
    p20.drop_tip()
#Plate on spot 6 needs column 2
    p20.pick_up_tip()
    p20.transfer(10, source_plate.columns()[2], plate_slot6.columns()[0], 
                 mix_before=(8,20),mix_after=(5,20), new_tip = "never")
    p20.drop_tip()
#Plate on spot 7 needs column 2   
    p20.pick_up_tip()
    p20.transfer(10, source_plate.columns()[2], plate_slot7.columns()[0], 
                 mix_before=(8,20),mix_after=(5,20),new_tip = "never")
    p20.drop_tip()
     
  
    
  
#Serial dilute (OBS leave out last column as there are the sterility controls)
# Discard 50 ul of last dilution step 

    for plate in Dest_plates:
        p300.pick_up_tip()
        p300.mix(3, 80, plate['A1'])
        for source, dest in zip(
                plate.columns()[0:9],
                plate.columns()[1:10]):
            p300.transfer(50, source, dest, new_tip='never',
                          mix_after=(5,80))
        p300.aspirate(50, plate['A10'])
        p300.drop_tip()

    protocol.comment("Run Complete")    



