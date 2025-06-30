"""
Test the precision of the Opentron compared to the flowrobot and handpipetting.

Version 1
owner: Troels Angelo
date: 2022.02.02

URL for kit: https://www.qiagen.com/gb/shop/automated-solutions/sample-disruption/rneasy-mini-kit/


Optimizations:
- Combine the two sets of code for 300ul & 20ul
- Consider setup


Questions 
- Do we see enough variance for us to consider triplicates?
"""

## 1. metadata
from itertools import count
import re


metadata = {
    'protocolName': 'PipetteprecisionPilot',
    'author': 'Name <s153564@student.dtu.dk>',
    'description': 'Test the precision of the Opentron compared to the flowrobot and handpipetting',
    'apiLevel': '2.8'
}


## 2. Functions used in the code

def get_values(*names):
    import json
    _all_values = json.loads("""{"plate_no":"3"}""")
    return [_all_values[n] for n in names]

def aspirate_counter(totalvolume, aspirateamount, pipetteheads):
    if totalvolume + aspirateamount * pipetteheads < 13500 :
        totalvolume += aspirateamount * pipetteheads
    else:
        totalvolume = 0
    return totalvolume

def wetting(times, volume, position, pipettename):
    for n in range(times):
        pipettename.flow_rate.aspirate = 150
        pipettename.flow_rate.dispense = 150
        pipettename.aspirate(volume, position.bottom(20))
        pipettename.dispense(volume, position.bottom(20))
        


## 3. protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol):
    [plate_no] = get_values('plate_no')

    ## 3. labware
    # labware names: https://labware.opentrons.com/

    microplate_type = 'nest_96_wellplate_200ul_flat'


    reagents_plate = protocol.load_labware('moas_12rows', '11')
    microplates = [protocol.load_labware(
                microplate_type, s) for s in ['7', '8', '9']]
    output_plate20ul = protocol.load_labware('corning_384_wellplate_112ul_flat', '6')

    # tips
    tip_rack_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '10')
    tip_rack_2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '5')

    ## 4. pipettes
    pipette_p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tip_rack_1])
    pipette_p20 = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tip_rack_2])

    reactantsize = [100, 150, 200]
    aspirate_total = 0
    reagents_well = ''
    aspirate_number = 0
    platecount = 0
    ## 5. commands  

    for plate in microplates[0:int(plate_no)]:
        pipette_p300.pick_up_tip()
        wetting(3, 200, reagents_plate['A12'], pipette_p300)
        pipette_p300.flow_rate.aspirate = 30
        pipette_p300.flow_rate.dispense = 30

        for dispense_pos in plate.rows()[0]:
            
            if aspirate_total == 0:
                aspirate_number += 1
                reagents_well = 'A' + str(aspirate_number)

            pipette_p300.move_to(reagents_plate[reagents_well].top(10))
            pipette_p300.default_speed = 200
            pipette_p300.aspirate(reactantsize[platecount], reagents_plate[reagents_well].bottom(1))
            pipette_p300.default_speed = None

            aspirate_total = aspirate_counter(aspirate_total, reactantsize[platecount], 8)

            pipette_p300.default_speed = 200
            pipette_p300.dispense(reactantsize[platecount], dispense_pos)
            pipette_p300.blow_out(dispense_pos.bottom(2))
            pipette_p300.default_speed = None
        
        pipette_p300.drop_tip()
        platecount += 1
        
    ################################ 20 ul #####################################

    volumecount = 0
    volumes = [5, 10, 20]

    ################################ Pre-filler #################################
    
    pipette_p20.pick_up_tip()
    wetting(3, 20, reagents_plate['A12'], pipette_p20)
    for dispense_pos in range(18):
        
        pipette_p20.move_to(reagents_plate['A5'].top(10))
        pipette_p20.default_speed = 150
        pipette_p20.aspirate(10, reagents_plate['A5'].bottom(10))

        pipette_p20.dispense(10, output_plate20ul.rows()[0][dispense_pos].bottom(4))
        pipette_p20.blow_out(output_plate20ul.rows()[0][dispense_pos].bottom(6))
        pipette_p20.default_speed = None

        pipette_p20.move_to(reagents_plate['A5'].top(10))
        pipette_p20.default_speed = 150
        pipette_p20.aspirate(10, reagents_plate['A5'].bottom(10))

        pipette_p20.dispense(10, output_plate20ul.rows()[1][dispense_pos].bottom(4))
        pipette_p20.blow_out(output_plate20ul.rows()[1][dispense_pos].bottom(6))
        pipette_p20.default_speed = None

    pipette_p20.return_tip()

    ################################ Actual filling ###############################

    pipette_p20.pick_up_tip()
    wetting(3, 20, reagents_plate['A12'], pipette_p20)

    for dispense_pos in range(18):

        if dispense_pos == 6 or dispense_pos == 12:
            pipette_p20.return_tip()
            pipette_p20.pick_up_tip()
            wetting(3, 20, reagents_plate['A12'], pipette_p20)
            volumecount += 1
        
        pipette_p20.move_to(reagents_plate['A5'].top(10))
        pipette_p20.default_speed = 150
        pipette_p20.aspirate(volumes[volumecount], reagents_plate['A5'].bottom(10))
        
        pipette_p20.dispense(volumes[volumecount], output_plate20ul.rows()[0][dispense_pos].bottom(4))
        pipette_p20.blow_out(output_plate20ul.rows()[0][dispense_pos].bottom(6))
        pipette_p20.default_speed = None

        pipette_p20.move_to(reagents_plate['A5'].top(10))
        pipette_p20.default_speed = 150
        pipette_p20.aspirate(volumes[volumecount], reagents_plate['A5'].bottom(10))

        pipette_p20.dispense(volumes[volumecount], output_plate20ul.rows()[1][dispense_pos].bottom(4))
        pipette_p20.blow_out(output_plate20ul.rows()[1][dispense_pos].bottom(6))
        pipette_p20.default_speed = None

    pipette_p20.return_tip()
