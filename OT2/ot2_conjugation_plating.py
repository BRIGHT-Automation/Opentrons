"""Conjugation plating: helper strain from a 50 mL tube + E. coli from a deep-well plate.

An Opentrons Protocol API v2 file for the OT-2 (p300 single), wrapped by this
package's ``run.py``. For every E. coli well in the first ``plate_count``
columns of the deep-well plate, with ONE tip:

1. ``helper_volume_ul`` of the helper strain (50 mL Falcon, A1 of the tube
   rack) goes into well A1 of the growth-profiler plate. The helper comes
   first: the tip has only touched the Falcon at this point,
2. ``ecoli_volume_ul`` of the E. coli well goes in on top of it, and the
   mix is pipetted up and down ``mix_repetitions`` times in place,
3. ``plate_volume_ul`` of the mix is plated into the next well of the 8-well plates.

Plates fill down the columns: deep-well column 1 (A1-H1) -> 8-well plate 1
(its 8 wells in order), column 2 -> plate 2, and so on. Six 8-well plates fit
on the deck, so the default run covers the first half (columns 1-6, 48 wells).

The tip goes into the E. coli well after the Falcon, which is fine because the E. coli
is used up in this run; the Falcon is never touched by a used tip. One tip per
conjugation: 48 for the default run, half a box.

The 8-well plate is the BRIGHT library's Thermo 267062 (namespace ``bright``): the
coordinator supplies it; in the Opentrons app, upload ``labware/thermo_267062.json``
with the protocol.
The runtime parameter ``variable_name``s match ``protocol.yaml``.
"""

from opentrons import protocol_api

requirements = {"robotType": "OT-2", "apiLevel": "2.20"}

metadata = {
    "protocolName": "Conjugation Plating",
    "author": "BRIGHT biofoundry",
    "description": (
        "Helper strain (50 mL tube) + E. coli (deep-well plate) mixed in a "
        "growth-profiler plate, then plated on 8-well plates."
    ),
}

PIPETTE = "p300_single_gen2"
TIPRACK = "opentrons_96_tiprack_300ul"
PLATE_8WELL = "thermo_267062"  # Nunc 8-well dish (library, namespace bright)
DEEP_WELL = (
    "thermoscientificnunc_96_wellplate_1300ul"  # Nunc 96 deep well 1.3 mL (stock)
)
TUBE_RACK = "opentrons_6_tuberack_falcon_50ml_conical"
# Stand-in until the Enzyscreen CR1496dg has a library definition (its footprint and
# well grid are still null in labware/): a flat-bottom 96 plate, only the depth differs.
MIX_PLATE = "corning_96_wellplate_360ul_flat"
MIX_WELL = "A1"

PLATE_SLOTS = ["1", "2", "3", "4", "5", "6"]  # 8-well plates, plate 1 first
TIPRACK_SLOT = "7"
DEEP_WELL_SLOT = "8"
TUBE_RACK_SLOT = "9"
MIX_PLATE_SLOT = "10"

MIX_VOLUME_UL = 150  # of the 200 uL in the mixing well
ASPIRATE_CLEARANCE_MM = 1.5  # above the bottom of tubes and wells
PLATE_DISPENSE_BELOW_RIM_MM = 3  # dispense just inside the rim, not onto the agar
HELPER_START_VOLUME_UL = 10000  # what the simulation assumes is in the tube
ECOLI_START_VOLUME_UL = 500  # per deep-well well, at least the E. coli volume


def add_parameters(parameters):
    parameters.add_float(
        variable_name="ecoli_volume_ul",
        default=100.0,
        minimum=20.0,
        maximum=200.0,
        display_name="E. coli volume",
        unit="uL",
    )
    parameters.add_float(
        variable_name="helper_volume_ul",
        default=100.0,
        minimum=20.0,
        maximum=200.0,
        display_name="Helper strain volume",
        unit="uL",
    )
    parameters.add_float(
        variable_name="plate_volume_ul",
        default=200.0,
        minimum=20.0,
        maximum=300.0,
        display_name="Total plate volume",
        description="Taken from the mix and plated; at most E. coli + helper volume",
        unit="uL",
    )
    parameters.add_int(
        variable_name="mix_repetitions",
        default=3,
        minimum=1,
        maximum=10,
        display_name="Mix repetitions",
    )
    parameters.add_int(
        variable_name="plate_count",
        default=6,
        minimum=1,
        maximum=6,
        display_name="8-well plates to fill",
        description="One deep-well column per plate, starting at column 1",
    )


def run(protocol: protocol_api.ProtocolContext):
    ecoli_volume = protocol.params.ecoli_volume_ul
    helper_volume = protocol.params.helper_volume_ul
    plate_volume = protocol.params.plate_volume_ul
    repetitions = protocol.params.mix_repetitions
    plate_count = protocol.params.plate_count
    in_well = ecoli_volume + helper_volume
    if plate_volume > in_well:
        raise ValueError(
            f"Total plate volume ({plate_volume} uL) is more than the mix holds "
            f"({in_well} uL = {ecoli_volume} E. coli + {helper_volume} helper)"
        )
    mix_volume = min(MIX_VOLUME_UL, in_well)

    tips = protocol.load_labware(TIPRACK, TIPRACK_SLOT, label="p300 tips")
    recipients = protocol.load_labware(DEEP_WELL, DEEP_WELL_SLOT, label="E. coli")
    rack = protocol.load_labware(TUBE_RACK, TUBE_RACK_SLOT, label="Helper strain")
    mix_plate = protocol.load_labware(
        MIX_PLATE, MIX_PLATE_SLOT, label="Growth profiler plate"
    )
    plates = [
        protocol.load_labware(
            PLATE_8WELL, slot, label=f"8-well plate {n}", namespace="bright"
        )
        for n, slot in enumerate(PLATE_SLOTS[:plate_count], start=1)
    ]
    pipette = protocol.load_instrument(PIPETTE, "right", tip_racks=[tips])

    helper = rack["A1"]
    mix_well = mix_plate[MIX_WELL]

    helper_liquid = protocol.define_liquid(
        "Helper strain", "Conjugation helper strain", "#2E8B57"
    )
    ecoli_liquid = protocol.define_liquid("E. coli", "E. coli cultures", "#D9A441")
    helper.load_liquid(helper_liquid, HELPER_START_VOLUME_UL)
    for column in recipients.columns()[:plate_count]:
        for well in column:
            well.load_liquid(ecoli_liquid, max(ECOLI_START_VOLUME_UL, ecoli_volume))

    protocol.comment(
        f"{plate_count * 8} conjugations: {helper_volume} uL helper + "
        f"{ecoli_volume} uL E. coli, {plate_volume} uL plated, {plate_count * 8} tips"
    )

    bottom = ASPIRATE_CLEARANCE_MM
    rim = -PLATE_DISPENSE_BELOW_RIM_MM
    for plate, column in zip(plates, recipients.columns()[:plate_count], strict=True):
        for target, ecoli in zip(plate.wells(), column, strict=True):
            pipette.pick_up_tip()
            # helper first, so the tip has only touched the Falcon
            pipette.aspirate(helper_volume, helper.bottom(bottom))
            pipette.dispense(helper_volume, mix_well.bottom(bottom))
            pipette.aspirate(ecoli_volume, ecoli.bottom(bottom))
            pipette.dispense(ecoli_volume, mix_well.bottom(bottom))
            pipette.mix(repetitions, mix_volume, mix_well.bottom(bottom))
            pipette.aspirate(plate_volume, mix_well.bottom(bottom))
            pipette.dispense(plate_volume, target.top(rim))
            pipette.blow_out(target.top(rim))
            pipette.drop_tip()
