metadata = {
    'protocolName': 'Multichanel test',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.2'
}

def run(protocol):

	#Load Tips1
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '9')]
    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    p20Multi = protocol.load_instrument("p20_multi_gen2", "right", tip_racks=tips20)
    p300Multi = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=tips300)

    p20Multi.pick_up_tip()
    p20Multi.return_tip()

    p300Multi.pick_up_tip()
    p300Multi.return_tip()
