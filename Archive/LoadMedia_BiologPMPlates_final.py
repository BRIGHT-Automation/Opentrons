# Modified from 'GP Load Glycerol Droplets', by Lachlan <lajamu@biosustain.dtu.dk

# To use this protocol for loading Biolog PM1, PM2 and PM3 plates, 
# load 12 mL of PM1,2 inoculation media in reservoir A1-6,
# and 12 mL of PM3 inoculation media in reservoir A7-9

metadata = {
    'protocolName': 'Load Biolog PM plates_final',
    'author': 'Casper <cluijt@biosustain.dtu.dk',
    'source': 'DTU Biosustain',
    'apiLevel': '2.2'
}


def run(protocol):
    
        #Load Tips
        tips200  = [protocol.load_labware('opentrons_96_filtertiprack_200ul', slot) for slot in [1]]
        
        #Load Pipettes
        p300Multi = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=tips200)
        
        #Load labware
        plates_pm1 = [
                protocol.load_labware("nest_96_wellplate_200ul_flat", slot)
                for slot in [ 2, 3, 4]]
        
        plates_pm2 = [
                protocol.load_labware("nest_96_wellplate_200ul_flat", slot)
                for slot in [ 6, 7, 8]]
        
        plates_pm3 = [
                protocol.load_labware("nest_96_wellplate_200ul_flat", slot)
                for slot in [ 9, 10, 11]]
    
        reservoir = protocol.load_labware("moas_12rows", 5)

        #Inoculate

        def load(src, dst):
            p300Multi.mix(1, 100, src.bottom(z=1)) # Mix medium before transferring to prevent spores from sedimenting
            p300Multi.transfer(100, src.bottom(z=1), dst.top(), rate=0.5, new_tip="never")
            p300Multi.blow_out(dst.top())  # Blow out to ensure all liquid is expelled
            # Adjust the z-coordinate to the appropriate depth for dipping
            p300Multi.move_to(dst.bottom(z=1))  # Moves to the bottom of the destination well (adjust z as needed)
            p300Multi.move_to(dst.top(z=5))  # Move back up to the top of the well (adjust z as needed)
            p300Multi.blow_out(dst.top())  # Blow out to ensure all liquid is expelled

        p300Multi.pick_up_tip()
        
        reservoir_well_index = 0
        for plate_index, p in enumerate(plates_pm1 + plates_pm2 + plates_pm3):
                reservoir_well = f"A{reservoir_well_index + 1}"
                for col_index, col in enumerate(p.columns()):
                        load(reservoir[reservoir_well], col[0])
                reservoir_well_index += 1
                
        p300Multi.drop_tip()