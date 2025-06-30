import opentrons
from opentrons import protocol_api

metadata = {'apilevel' : '2.16',
            'protocolName': 'Coco - Saccharomyces transformation with cells and mix dispense',
            'fileName': 'transformation_dispensing.py',
            'author': 'Jaime <jmutr@dtu.dk>'}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}



def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 8)
    plate_dna = protocol.load_labware('armadillo_96_wellplate_200ul_pcr_full_skirt', 4)
    plate_mix = protocol.load_labware('corning_96_wellplate_360ul_flat', 6)
    plate_cells = protocol.load_labware('corning_96_wellplate_360ul_flat', 5)
    plate_dispensing = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', 9)
    pip300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips]) 


    # dispense cells first
    def disp_cells():
        for i in range(12):
            col_dna = plate_dna.columns()[i]
            col_cells = plate_cells.columns()[i]
            col_mix = plate_mix.columns()[i]    
            
            if i == 0:
                pip300.pick_up_tip(tips.columns()[0][0])
                pip300.aspirate(150, plate_dispensing.columns()[0][0].bottom(z=1), rate=0.3)
            elif i == 6:
                pip300.aspirate(150, plate_dispensing.columns()[0][0].bottom(z=1), rate=0.3)
            pip300.dispense(25, col_cells[0])
            if i == 11:
                pip300.return_tip()
        
    
    # dispense mix second
    def disp_mix(): 
        for i in range(12):
            col_dna = plate_dna.columns()[i]
            col_cells = plate_cells.columns()[i]
            col_mix = plate_mix.columns()[i]

            if i == 0:
                pip300.pick_up_tip(tips.columns()[11][0])
            pip300.aspirate(150, plate_dispensing.columns()[11][0].bottom(z=0.5), rate=0.1)
            pip300.dispense(150, col_mix[0])
            pip300.blow_out(col_mix[0].top())
            if i == 11:
                pip300.return_tip()


    # do the transformation
    def transformation1():
        for i in range(12):
            col_dna = plate_dna.columns()[i]
            col_cells = plate_cells.columns()[i]
            col_mix = plate_mix.columns()[i]
            
            pip300.pick_up_tip(tips.columns()[i][0])
            pip300.aspirate(30, col_cells[0].bottom(z=1), rate=0.3)
            pip300.dispense(30, col_dna[0])
            pip300.mix(2, 20, col_dna[0])

            pip300.aspirate(45, col_dna[0].bottom(z=1), rate=0.3)
            pip300.dispense(45, col_cells[0])

            pip300.aspirate(150, col_mix[0].bottom(z=1), rate=0.1)
            pip300.dispense(150, col_cells[0], rate=0.1)
            pip300.mix(3, 50, col_cells[0], rate=0.2)
            pip300.blow_out(col_cells[0])
            pip300.return_tip()

    
    def transformation():
        for i in range(12):
            col_dna = plate_dna.columns()[i]
            col_cells = plate_cells.columns()[i]
            col_mix = plate_mix.columns()[i]
            
            pip300.pick_up_tip(tips.columns()[i][0])
            pip300.aspirate(25, plate_dispensing.columns()[0][0].bottom(z=0.5), rate=0.1)
            pip300.dispense(25, col_dna[0])
            pip300.mix(2, 20, col_dna[0])

            pip300.aspirate(50, col_dna[0].bottom(z=0.5), rate=0.1)
            pip300.dispense(50, col_cells[0])

            pip300.aspirate(150, col_mix[0].bottom(z=0.5), rate=0.1)
            pip300.dispense(150, col_cells[0], rate=0.3)
            pip300.mix(3, 50, col_cells[0], rate=0.2)
            pip300.blow_out(col_cells[0])
            pip300.return_tip()

    disp_mix()
    transformation()