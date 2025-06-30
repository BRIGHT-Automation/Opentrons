metadata = {
    'protocolName': 'Multichanel + Single Channel test',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.2'
}

def run(protocol):

	#Load Tips1
    tips300_single= [protocol.load_labware('opentrons_96_tiprack_300ul', '9')]
    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    p300gen1 = protocol.load_instrument("p300_single", "right", tip_racks=tips300_single)
    p300Multi = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=tips300)

    p300gen1.pick_up_tip()
    p300gen1.return_tip()

    p300Multi.pick_up_tip()
    p300Multi.return_tip()
