#This protocol takes 
#   8 x 96 well plates (4 x skirted 200 uL PCR plates, 4 x non skirted sarstedt 200uL PCR plates on aluminium block) 
#   a 12 columns plate containing 
#       col 1 : 13ml  lysis buffer
#       col 2 : 9 ml 16s PCR1 Master Mix

#Run time for 8 plates around 14 minutes
#        
# Requires 1x 20 µL Tip racks 

from opentrons import protocol_api

metadata = {
    'protocolName': '16s_plate_prep',
    'author': 'Jeremy Armetta',
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    # Load a P20 multi on the left slot
    tips20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul', '3'), 
              protocol.load_labware('opentrons_96_filtertiprack_20ul', '6'), 
              protocol.load_labware('opentrons_96_filtertiprack_20ul', '9')]
    p20Multi = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=tips20)

    lysis_plate_1 = protocol.load_labware('sarstedt_96_aluminumblock_200ul', '1', label='Lysis plate 1')
    lysis_plate_2 = protocol.load_labware('sarstedt_96_aluminumblock_200ul', '4', label='Lysis plate 2')
    lysis_plate_3 = protocol.load_labware('sarstedt_96_aluminumblock_200ul', '7', label='Lysis plate 3')

    
    PCR_plate_1 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2', label='PCR plate 1')
    PCR_plate_2 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5', label='PCR plate 2')
    PCR_plate_3 = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '8', label='PCR plate 3')


    columns = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']
    
    def fill_set_plates():

        for well in columns:
            p20Multi.pick_up_tip()
            p20Multi.flow_rate.aspirate = 5
            p20Multi.flow_rate.dispense = 5
            p20Multi.transfer(1,lysis_plate_1.wells_by_name()[well].bottom(z=5), PCR_plate_1.wells_by_name()[well].bottom(z=1.1), new_tip='never', blow_out=True, blowout_location='destination well')
            p20Multi.flow_rate.aspirate = 15
            p20Multi.flow_rate.dispense = 15
            p20Multi.mix(5, 8, PCR_plate_1.wells_by_name()[well].bottom(z=1.6))
            p20Multi.drop_tip()

        for well in columns:
            p20Multi.pick_up_tip()
            p20Multi.flow_rate.aspirate = 5
            p20Multi.flow_rate.dispense = 5
            p20Multi.transfer(1,lysis_plate_2.wells_by_name()[well].bottom(z=5), PCR_plate_2.wells_by_name()[well].bottom(z=1.1), new_tip='never', blow_out=True, blowout_location='destination well')
            p20Multi.flow_rate.aspirate = 15
            p20Multi.flow_rate.dispense = 15
            p20Multi.mix(5, 8, PCR_plate_2.wells_by_name()[well].bottom(z=1.6))
            p20Multi.drop_tip()
        
        for well in columns:
            p20Multi.pick_up_tip()
            p20Multi.flow_rate.aspirate = 5
            p20Multi.flow_rate.dispense = 5
            p20Multi.transfer(1,lysis_plate_3.wells_by_name()[well].bottom(z=5), PCR_plate_3.wells_by_name()[well].bottom(z=1.1), new_tip='never', blow_out=True, blowout_location='destination well')
            p20Multi.flow_rate.aspirate = 15
            p20Multi.flow_rate.dispense = 15
            p20Multi.mix(5, 8, PCR_plate_3.wells_by_name()[well].bottom(z=1.6))
            p20Multi.drop_tip()
    
    fill_set_plates()
    protocol.comment('Run completed')
