# This protocol transfers 12 columns from a 96 wp into 1 column of a 96 wp, for prepoling before PCR cleanup
# It takes 
#   6 x 96 well plates (skirted 200 uL PCR plates) 
#   a destination plate (skirted 200 uL PCR plate) for clean up

#Run time = about 9 min
#        
# Requires 1x 20 µL Tip racks 

from opentrons import protocol_api

metadata = {
    'protocolName': 'plate_pooling_12_to_1',
    'author': 'Jeremy Armetta',
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    # Load a P20 multi on the left slot
    tips20 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '9')
    p20Multi = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tips20])

    prepooling_plate_1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '10', label='prepooling plate')
    prepooling_plate_2 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '11', label='prepooling plate')
    
    PCR_plate_1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '1', label='PCR plate 1')
    PCR_plate_2 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2', label='PCR plate 2')
    PCR_plate_3 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '3', label='PCR plate 3')
    PCR_plate_4 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '4', label='PCR plate 4')
    PCR_plate_5 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5', label='PCR plate 5')
    PCR_plate_6 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6', label='PCR plate 6')

    p20Multi.flow_rate.aspirate = 10
    p20Multi.flow_rate.dispense = 20

    columns = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']
    
    def prepooling():

        #consolidate the first plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_1.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A1'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_1.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A1'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the second plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_2.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A2'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_2.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A2'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the third plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_3.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A3'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_3.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A3'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the fourth plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_4.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A4'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_4.wells_by_name()[well_name].bottom(1) for well_name in columns],prepooling_plate_2.wells_by_name()['A4'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the fith plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_5.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A5'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_5.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A5'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the sixth plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_6.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A6'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_6.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A6'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        protocol.pause(msg="First half of the run complete. Please load the six other plates to be pooled")

        #consolidate the first plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_1.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A7'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_1.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A7'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the second plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_2.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A8'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_2.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A8'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the third plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_3.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A9'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_3.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A9'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the fourth plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_4.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A10'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_4.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A10'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the fith plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_5.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A11'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_5.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A11'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()

        #consolidate the sixth plate
        p20Multi.pick_up_tip()
        p20Multi.consolidate(5, [PCR_plate_6.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_1.wells_by_name()['A12'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.consolidate(5, [PCR_plate_6.wells_by_name()[well_name].bottom(0.5) for well_name in columns],prepooling_plate_2.wells_by_name()['A12'], new_tip='never', blow_out=True, blowout_location='destination well')
        p20Multi.drop_tip()
    
    prepooling()
    protocol.comment('Run completed')