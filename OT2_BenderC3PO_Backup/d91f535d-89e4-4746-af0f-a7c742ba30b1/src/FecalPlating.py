metadata = {
    'protocolName': 'Fecal Plating and Dilution',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.2'
}

def run(protocol):

	#Load Tips1
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '9')]
    tips20_2 = [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]

    p20Multi = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=tips20)
    p1000Single = protocol.load_instrument("p20_single_gen2", "right", tip_racks=tips20_2)

    temp_block = protocol.load_module("tempdeck", 4)
    temp_block.set_temperature(4)

    pooTubes = temp_block.load_labware("opentrons_24_aluminumblock_nest_2ml_screwcap", label="PooTubes")

    plate_type = "corning_96_wellplate_360ul_flat"
    locs = [10, 11, 5, 6]

    dilutionPlates = [protocol.load_labware(plate_type, slot, label="Dilution Plates")
    				for slot in locs]

    agar_plate_type = "biorad_96_wellplate_200ul_pcr" #can be any 96 that isn't the same as dil plate
    agar_locs = [7, 8, 2, 3]
    agar_plates = [protocol.load_labware(agar_plate_type, slot, label="Agar")
    				for slot in agar_locs]

    # for p in range(16):
    # 	p1000Single.distribute(10, pooTubes.wells()[p], [dilutionPlates[0].wells()[p], 
    # 		dilutionPlates[1].wells()[p]] if p < 8 
    # 		else [dilutionPlates[2].wells()[p-8], dilutionPlates[3].wells()[p-8]])
           
            
        
    def spot(dest, spot_vol):
        """Takes a diluted transformed culture and spots the defined volume onto agar 
        in a Nunc omnitray"""

        SAFE_HEIGHT = 15  
        spotting_dispense_rate=0.025 
        p20Multi.move_to(dest.top(SAFE_HEIGHT))
        protocol.max_speeds["Z"] = 50
        p20Multi.move_to(dest.top(2))
        p20Multi.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p20Multi.move_to(dest.top(0))
        del protocol.max_speeds["Z"]
    
    def spot_then_dilute(sourceCol, agar_dest, destcol, spot_vol):
        p20Multi.aspirate(spot_vol, sourceCol)
        spot(agar_dest, spot_vol)
        p20Multi.transfer(10, sourceCol, destcol, mix_after=(5, 20), new_tip="never")
        
    
    def spot_dilute_plate(plate, agar, spot_vol):
        p20Multi.pick_up_tip()
        for col in range(1, 10):
            w = "A"+str(col)
            x = "A" + str(col+1)
            spot_then_dilute(plate[w], agar[w], 
                             plate[x], spot_vol)
            #Spot final dilution THIS S THE PROBLEM, DOUBLE UP WITH LINE 52-55
        p20Multi.aspirate(spot_vol, plate[x])
        spot(agar[x], spot_vol)
        p20Multi.drop_tip()
        
    for pl, ag in zip(dilutionPlates, agar_plates):
        spot_dilute_plate(pl, ag, 5)
        
    protocol.comment("Run Complete!")
        
        


    

