########################
#Keep this the same in all code
from opentrons import simulate
from opentrons import execute
from opentrons import protocol_api


# Define Opentrons protocol
metadata = {'apiLevel': '2.13'}
sim_protocol = simulate.get_protocol_api('2.13')

#Functions for OT
def transfer_volume(pipette, source_location, destination_well, volume, air_gap_volume):
    pipette.aspirate(volume, source_location)
    pipette.air_gap(air_gap_volume)  # Aspirate air to create an air gap
    pipette.dispense(volume + air_gap_volume, destination_well)  # Dispense liquid along with the air gap
    
def fill_wells_sanger_style(p300_multi, p300_single, working_plate, sanger_plate, volume=15):
    # Wells to be transferred with the multichannel pipette
    multichannel_wells = ['A1', 'A2', 'A3', 'A5', 'A6', 'A7', 'A9', 'A10', 'A11']
    # Columns to be transferred with the single-channel pipette
    singlechannel_cols = ['4', '8', '12']

    # Transfer using the multichannel pipette
    for well_name in multichannel_wells:
        p300_multi.pick_up_tip()
        source_well = working_plate.wells_by_name()[well_name]
        destination_well = sanger_plate.wells_by_name()[well_name]
        p300_multi.flow_rate.aspirate = 200  # set aspirate speed to 200 µL/s
        p300_multi.aspirate(volume, source_well.bottom(z=2))
        p300_multi.dispense(volume, destination_well.bottom())
        p300_multi.blow_out(destination_well.bottom(z=4))  # Blow out at the top of the destination well
        p300_multi.drop_tip()

    # Transfer using the single-channel pipette
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for col in singlechannel_cols:
        for row in rows:
            # Skip wells in the 32nd row
            if row == 'H' and col in ['4', '8', '12']:
                continue
            well_name = f"{row}{col}"
            source_well = working_plate.wells_by_name()[well_name]
            destination_well = sanger_plate.wells_by_name()[well_name]
            p300_single.pick_up_tip()
            p300_single.flow_rate.aspirate = 200  # set aspirate speed to 200 µL/s
            p300_single.aspirate(volume, source_well.bottom(z=2))
            p300_single.dispense(volume, destination_well.bottom())
            p300_single.blow_out(destination_well.bottom(z=4))  # Blow out at the top of the destination well

            p300_single.drop_tip()

def transfer_section(source_well_name, section, pipette, reagents, plate, volume=26, air_gap_volume=10, mix_vol=20): # Added air_gap_volume as a default parameter
    for col in section:
        pipette.pick_up_tip()
        mix_transfer_volume(pipette, reagents.wells_by_name()[source_well_name], plate.wells_by_name()[col], volume, air_gap_volume, mix_repetitions=1, mix_volume=mix_vol)
        pipette.drop_tip()

#Run OT Protocol 
def run(protocol: protocol_api.ProtocolContext):
    #Temperature module with the plate for the colonies 
    temp_mod_1 = protocol.load_module(module_name='temperature module',location=10)
    working_plate = temp_mod_1.load_labware(name='opentrons_96_aluminumblock_nest_wellplate_100ul')
    sanger_plate= protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5')

    #Reagents in the 2 ml Epp tubes– make sure these are open before starting protocol. For use with single channel
    two_ml_reagents = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap', '8')  
    #A1:primer 1
    #A2: primer 2
    #A3: primer 3
    #C1: MM 1
    #C2: MM 2
    #C3: MM3
    #Load trough with bulk reagents to be added with multi-channel
    trough = protocol.load_labware('nest_12_reservoir_15ml', '11')

    #Load final seq plates 

    # Load tip racks
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', location='2')
    tiprack_3 = protocol.load_labware('opentrons_96_tiprack_300ul', location='3')


    #Load pipettes
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack_1,tiprack_2])
    p300_single=protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_3])
    
    cols_to_fill = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12'] 
    #Break plate up into sections so you skip every 32nd well 
    size = len(cols_to_fill) // 3
    first_section = cols_to_fill[:size]
    second_section = cols_to_fill[size:2*size]
    third_section = cols_to_fill[2*size:]
    
    multichannel_cols = [1, 2, 3, 5, 6, 7, 9, 10, 11]
    singlechannel_cols = [4, 8, 12]

# Transfer 15ul of PCR into the sanger plate, leaving H4, H8, and H12 empty
    fill_wells_sanger_style(p300_multi, p300_single, working_plate, sanger_plate)
    
