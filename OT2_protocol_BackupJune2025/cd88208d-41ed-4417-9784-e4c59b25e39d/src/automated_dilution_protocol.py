
from opentrons import protocol_api

metadata = {
    'protocolName': 'Add water and Dilute Oligos in Tubes',
    'author': 'Tu Nombre <tu.email@ejemplo.com>',
    'description': 'Añadir agua a tubos con primers, resuspender y hacer una dilución 1:10 en otros tubos, cambiando punta en cada transferencia',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):
    # Datos de nmoles
    nmols = {
        'A1': 23.7, 'A2': 26.8, 'A3': 34.6, 'A4': 32.4, 'A5': 27.3, 'A6': 24.5, 'A7': 22.5,'B1': 20.9, 'B2': 27.0, 'B3': 24.8, 'B4': 27.6, 'B5': 24.6, 'B6': 29.6, 'B7': 19.8,'C1': 25.7, 'C2': 27.5, 'C3': 27.0, 'C4': 29.9, 'C5': 26.4, 'C6': 32.9, 'C7': 27.6,'D1': 16.9, 'D2': 29.4, 'D3': 22.7, 'D4': 29.8, 'D5': 23.8, 'D6': 25.8, 'D7': 30.1,'E1': 37.3, 'E2': 27.2, 'E3': 23.0, 'E4': 26.4, 'E5': 26.8, 'E6': 27.7, 'E7': 22.6,'F1': 35.9, 'F2': 27.5, 'F3': 19.5, 'F4': 29.8, 'F5': 29.5, 'F6': 25.9, 'G1': 36.9
    }

    # Definir el labware
    tips1000 = [protocol.load_labware("geb_96_tiprack_1000ul", 1)]
    tips20 = [protocol.load_labware("opentrons_96_filtertiprack_20ul", 3)]
    p1000 = protocol.load_instrument('p1000_single', 'right', tip_racks=tips1000)
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips20)
    
    oligo_rack = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 2)
    dilution_rack = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 4)
    water_rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", 5)
    water = water_rack["A1"]

    # Añadir 180 µL de agua a los tubos de dilución
    for well in nmols.keys():
        p1000.transfer(180, water, dilution_rack[well])

    # Resuspender primers en los tubos de oligos
    for well, nmol in nmols.items():
        p1000.pick_up_tip()
        p1000.transfer(nmol * 10, water, oligo_rack[well], mix_after=(5, 800))
        p1000.drop_tip()

    # Transferir una alícuota de resuspensión a los tubos de dilución (20 µL en 180 µL de agua)
    for well in nmols.keys():
        p20.pick_up_tip()
        p20.transfer(20, oligo_rack[well], dilution_rack[well], mix_after=(5, 20), new_tip='always')
        p20.drop_tip()
