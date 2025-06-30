metadata = {
    'protocolName': 'Saccharomyces Transformation',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}

#To update
#Add pause
#Change labware


def run(protocol):

    #Set volumes
    dna_volume = 5
    culture_vol = 14
    trans_mix_vol = 70

    #Load Tips1
    tips20_multi = [protocol.load_labware('opentrons_96_tiprack_20ul', '6')]
    tips20 = [
        protocol.load_labware('opentrons_96_tiprack_20ul', x) for x in ['3']
    ]

    #Load pippettes
    p20Multi = protocol.load_instrument("p20_multi_gen2",
                                        "left",
                                        tip_racks=tips20_multi)
    p20Single = protocol.load_instrument("p20_single_gen2",
                                         tip_racks=tips20,
                                         mount="right")

    #Load labware
    plate_type = "biorad_96_wellplate_200ul_pcr"
    transformation = protocol.load_labware(plate_type,
                                           1,
                                           label="Transformation Plate")
    rack = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        2,
        label="DNA Rack")
    reservoir = protocol.load_labware("corning_96_wellplate_360ul_flat", 4)
    culture = reservoir.wells()[0]

    #Functions to add dna to a row and column

    def add_dna_col(col, source, vol):
        for i in range(8):
            p20Single.pick_up_tip()
            p20Single.aspirate(vol, rack.wells()[source])
            p20Single.dispense(vol, transformation.columns()[col][i])
            p20Single.drop_tip()

    def add_dna_row(row, source, vol):
        p20Single.pick_up_tip()
        for i in range(10):
            p20Single.transfer(vol,
                               rack.wells()[source],
                               transformation.columns()[i][row],
                               new_tip="never",
                               touch_tip=True)
        p20Single.drop_tip()

    #Add plasmids to transformation plate
    #by row (including blank)
    for i in range(8):
        add_dna_row(i, i, dna_volume)

    #Add plasmids to transformation plate
    #by column (including blank)
    for i in range(10):
        add_dna_col(i, i + 8, dna_volume)

    p20Single.transfer(dna_volume,
                       rack["A1"],
                       transformation["A11"],
                       touch_tip=True)
    p20Single.transfer(dna_volume,
                       rack["C1"],
                       transformation["B11"],
                       touch_tip=True)

    protocol.pause('Add culture to plate')

    #Add culture to transformation plate
    for i in range(10):
        p20Multi.transfer(culture_vol,
                          culture,
                          transformation.columns()[i][0],
                          mix_before=(2, 20),
                          mix_after=(3, 20),
                          new_tip="always")
    p20Single.transfer(culture_vol, culture, transformation["A11"])
    p20Single.transfer(culture_vol, culture, transformation["B11"])
