metadata = {
    'apiLevel': '2.8',
    'protocolName': 'MagdeckHeightTest',
    'author': 'Lachlan Munro (lajamu@biosustain.dtu.dk',
}


#Parts of protocol modified from Opentrons protocol library

#Set number of samples (Note that protocol will run full columns)


def run(ctx):

    nCols = 1

    mag_deck = ctx.load_module('magnetic module gen2', '4')
    mag_deck.disengage()
    mag_plate = mag_deck.load_labware(
        'armadillo_pcr_200')

    mag_deck.engage(height=11)
    ctx.delay(60)
    mag_deck.disengage()