
metadata = {
    'protocolName': 'Carlos - heatshock cooling only',
    'fileName': 'heatshock.py',
    'author': 'Jaime <jmutr@dtu.dk>',
    'source': 'DTU Biosustain',
    'apiLevel': '2.16'
}

import math

def run(protocol):

    # def labware
    tips1 = protocol.load_labware('opentrons_96_tiprack_300uL', 10)
    tips2 = protocol.load_labware('opentrons_96_tiprack_300uL', 11)

    cells_res = protocol.load_labware('nest_96_wellplate_2ml_deep', 1) 
    media_res = protocol.load_labware('nest_1_reservoir_195ml', 9)

    cool_mod1 = protocol.load_module('temperature module gen2', 7)
    cool_ad1 = cool_mod1.load_adapter('opentrons_96_well_aluminum_block')
    dna_plate1 = cool_ad1.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')


    cool_mod2 = protocol.load_module('temperature module gen2', 4)
    cool_ad2 = cool_mod2.load_adapter('opentrons_96_well_aluminum_block')
    dna_plate2 = cool_ad2.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')
        
    #heat_mod = protocol.load_module('temperature module gen2', 9)
    #heat_ad = heat_mod.load_adapter('opentrons_96_well_aluminum_block')
    #transf_plate = heat_ad.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')

    final_plate1 = protocol.load_labware('nest_96_wellplate_2ml_deep', 5)
    final_plate2 = protocol.load_labware('nest_96_wellplate_2ml_deep', 8)

    pip = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips1, tips2])

    # variables
    n_col1 = 12
    n_col2 = 5
    cells_vol = 50
    final_media = 1000
    dna_vol = 10
    celldna_vol = cells_vol + dna_vol
    
    

    # actual protocol
    def heating_modules():
        cool_mod2.set_temperature(4)
        cool_mod1.set_temperature(4)
        cool_mod2.set_temperature(4)
        #heat_mod.set_temperature(42)



    # first we add the cells to the pre cooled dna plate
    def add_cells(n_col1, n_col2, cells_vol, plate_number):
        protocol.pause("Please, put the precooled media reservoir, DNA plate and competent cells. Then, press 'Resume'")
        
        if plate_number == 1:
            tips = tips1
            plate = dna_plate1
            n_col = n_col1
        elif plate_number == 2:
            tips = tips2
            plate = dna_plate2
            n_col = n_col2

        for i in range(n_col): 
            pip.pick_up_tip(tips.columns()[i][0])
            pip.aspirate(cells_vol, cells_res.columns()[0][0].bottom(z=1), rate=0.3)
            pip.dispense(cells_vol, plate.columns()[i][0], rate=0.8)
            pip.mix(2, cells_vol/2, plate.columns()[i][0], rate=0.7)
            pip.blow_out(plate.columns()[i][0].top())
            pip.return_tip()

        protocol.pause("Please, recover your competent cells (if you want jajaj). Then, press 'Confirm and resume'")

    # now we have to add the media in the final plate 
    def add_media(n_col1, n_col2, final_media, plate_number):
        rep = math.ceil(final_media / 300)
        vol = 1000 / rep      
        pip.pick_up_tip(tips2.columns()[11][0])  # reuse one tip column
        if plate_number == 1:
            n_col = n_col1
            final_plate = final_plate1
        elif plate_number == 2:
            n_col = n_col2
            final_plate = final_plate2
        
        for i in range(n_col):
            for j in range(4):
                pip.aspirate(vol, media_res.columns()[0][0], rate=0.8)
                pip.dispense(vol, final_plate.columns()[i][0])

        pip.return_tip()


    def heatshock():
        protocol.delay(minutes=15)
        protocol.pause("Whenever you are ready, make the heatshock yourself!. Then, press 'Confirm and resume'")
        protocol.delay(minutes=5)
    # okay, now that should have taken enough time for the dna and cells to bind etc
    
    # the heatshock should have been done manually
    # so now its just reusing the tips to put the dna in the final plate
    def inoculate_plate(n_col1, n_col2, celldna_vol, plate_number):
        if plate_number == 1:
            tips = tips1
            dna_plate = dna_plate1
            n_col = n_col1
            final_plate = final_plate1
        elif plate_number == 2:
            tips = tips2
            dna_plate = dna_plate2
            n_col = n_col2
            final_plate = final_plate2

        for i in range(n_col): 
            pip.pick_up_tip(tips.columns()[i][0])
            pip.aspirate(cells_vol, dna_plate.columns()[i][0].bottom(z=1), rate=0.3)
            pip.dispense(cells_vol, final_plate.columns()[i][0], rate=0.8)
            pip.mix(2, cells_vol/2, final_plate.columns()[i][0], rate=0.7)
            pip.blow_out(final_plate.columns()[i][0].top())
            pip.return_tip()

    

    
    # now the actual protocol
    heating_modules()
    #add_cells(n_col1, n_col2, cells_vol, 1)
    #add_cells(n_col1, n_col2, cells_vol, 2)
    #add_media(n_col1, n_col2, final_media, 1)
    #add_media(n_col1, n_col2, final_media, 2)
    #heatshock()
    #inoculate_plate(n_col1, n_col2, celldna_vol, 1)
    #inoculate_plate(n_col1, n_col2, celldna_vol, 2)