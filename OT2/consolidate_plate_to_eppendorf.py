from opentrons import protocol_api

metadata = {
    'protocolName': 'Consolidate 96-Well PCR Plate to Eppendorf',
    'author': 'Custom',
    'description': 'Consolidate 10 uL from each well of a 96-well PCR plate into a single Eppendorf tube, 2 columns (24 wells) at a time.',
    'apiLevel': '2.15'
}

def run(protocol: protocol_api.ProtocolContext):

    # ---------- LABWARE ----------
    pcr_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 1, 'PCR Plate')
    tube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2, 'Tube Rack')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 3, '300 uL Tip Rack')

    # ---------- PIPETTE ----------
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

    # ---------- PARAMETERS ----------
    aspiration_vol = 10       # uL per well
    mix_reps = 5              # mix repetitions when dispensing into eppendorf
    mix_vol = 200             # uL to mix with in eppendorf
    aspirate_rate = 0.5       # slower aspirate for small volumes (relative)
    dispense_height = 5       # mm above bottom when dispensing into eppendorf

    # ---------- DESTINATIONS ----------
    eppendorf = tube_rack.wells_by_name()['A1']

    # ---------- BUILD COLUMN PAIRS ----------
    # Columns 1-12, processed in pairs: (1,2), (3,4), (5,6), (7,8), (9,10), (11,12)
    all_columns = pcr_plate.columns()  # list of 12 columns, each with 8 wells
    column_pairs = [
        (all_columns[i], all_columns[i + 1])
        for i in range(0, 12, 2)
    ]

    # ---------- RUN ----------
    p300.pick_up_tip()

    # Set slower aspirate flow rate for accuracy with small volumes
    p300.flow_rate.aspirate = p300.flow_rate.aspirate * aspirate_rate

    for pair_idx, (col_a, col_b) in enumerate(column_pairs):
        wells_in_pair = col_a + col_b  # 16 wells (8 + 8) — wait, 2 cols = 16 wells

        # Aspirate 10 uL from each of the 24 wells... 
        # NOTE: 2 columns = 16 wells × 10 uL = 160 uL per cycle
        # If you truly want 24 wells (3 columns) per cycle, adjust below.
        # Current setup: 2 columns = 16 wells per cycle.

        for well in wells_in_pair:
            p300.aspirate(aspiration_vol, well.bottom(1))

        # Dispense into Eppendorf
        p300.dispense(p300.current_volume, eppendorf.bottom(dispense_height))

        # Mix to ensure all liquid is expelled from the tip
        p300.mix(mix_reps, min(mix_vol, p300.current_volume + 100), eppendorf.bottom(2))

        # Blow out to clear any residual
        p300.blow_out(eppendorf.top(-5))

        # Touch tip to remove droplets
        p300.touch_tip(v_offset=-3)

        protocol.comment(f'Completed column pair {pair_idx + 1}/6 '
                         f'(columns {pair_idx * 2 + 1}-{pair_idx * 2 + 2})')

    p300.drop_tip()

    protocol.comment('Protocol complete! All samples consolidated into Eppendorf A1.')
