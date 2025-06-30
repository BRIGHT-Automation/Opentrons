import opentrons
from opentrons import protocol_api

metadata = {'apilevel' : '2.16',
            'protocolName': 'Coco - Saccharomyces transformation',
            'fileName': 'transformation.py',
            'author': 'Jaime <jmutr@dtu.dk>'}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}



def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 8)
    plate_dna = protocol.load_labware('armadillo_96_wellplate_200ul_pcr_full_skirt', 4)
    plate_mix = protocol.load_labware('corning_96_wellplate_360ul_flat', 6)
    plate_cells = protocol.load_labware('corning_96_wellplate_360ul_flat', 5)

    pip300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips]) 

    for i in range(12):
        col_dna = plate_dna.columns()[i]
        col_cells = plate_cells.columns()[i]
        col_mix = plate_mix.columns()[i]
        
        pip300.pick_up_tip()
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