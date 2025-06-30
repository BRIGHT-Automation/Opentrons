# -*- coding: utf-8 -*-
"""
Created on 26-08-2024

@author Kai Kabuth
"""

metadata = {
    "protocolName": "C/N/P Optimization Media Set-Up",
    "author": "Kai Kabuth <kjokab@dtu.dk>",
    "apiLevel": "2.8",
}

# Phosphate Buffer: 5 mM
# Ammonia Buffer: 25 mM
# ddWater
# Carbon Buffer 10x: 1000 mM KOAc + 400 mM MOPS + TES

from opentrons import protocol_api

# µL of phosphate, ammonia, carbon, water
# Opentron pipetts in order A1 -> B1 -> C1 -> ... -> A2 -> B2 -> ...
media_recipe = [
    [20, 20, 50, 410],
    [20, 20, 50, 410],
    [20, 20, 50, 410],
    [20, 100, 50, 330],
    [20, 100, 50, 330],
    [20, 100, 50, 330],
    [20, 200, 50, 230],
    [20, 200, 50, 230],
    [20, 200, 50, 230],
    [20, 200, 50, 230],
    [100, 20, 50, 330],
    [100, 20, 50, 330],
    [100, 20, 50, 330],
    [100, 100, 50, 250],
    [120, 120, 50, 210],
    [120, 120, 50, 210],
    [120, 120, 50, 210],
    [120, 200, 50, 130],
    [120, 200, 50, 130],
    [200, 20, 50, 230],
    [200, 20, 50, 230],
    [200, 20, 50, 230],
    [200, 20, 50, 230],
    [200, 100, 50, 150],
    [200, 120, 50, 130],
    [200, 200, 50, 50],
    [200, 200, 50, 50],
    [200, 200, 50, 50],
    [200, 200, 50, 50],
    [30, 30, 75, 615],
    [30, 30, 75, 615],
    [30, 30, 75, 615],
    [30, 150, 75, 495],
    [30, 150, 75, 495],
    [30, 180, 75, 465],
    [30, 300, 75, 345],
    [30, 300, 75, 345],
    [150, 30, 75, 495],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 180, 75, 345],
    [150, 300, 75, 225],
    [150, 300, 75, 225],
    [150, 300, 75, 225],
    [150, 300, 75, 225],
    [180, 30, 75, 465],
    [180, 30, 75, 465],
    [180, 150, 75, 345],
    [180, 150, 75, 345],
    [180, 150, 75, 345],
    [180, 150, 75, 345],
    [180, 150, 75, 345],
    [180, 180, 75, 315],
    [180, 180, 75, 315],
    [180, 180, 75, 315],
    [180, 180, 75, 315],
    [300, 30, 75, 345],
    [300, 30, 75, 345],
    [300, 150, 75, 225],
    [300, 150, 75, 225],
    [300, 150, 75, 225],
    [300, 150, 75, 225],
    [300, 300, 75, 75],
    [300, 300, 75, 75],
    [40, 40, 100, 820],
    [40, 40, 100, 820],
    [40, 40, 100, 820],
    [40, 200, 100, 660],
    [40, 200, 100, 660],
    [40, 200, 100, 660],
    [40, 400, 100, 460],
    [40, 400, 100, 460],
    [40, 400, 100, 460],
    [40, 400, 100, 460],
    [200, 40, 100, 660],
    [200, 40, 100, 660],
    [200, 40, 100, 660],
    [200, 400, 100, 300],
    [240, 200, 100, 460],
    [240, 240, 100, 420],
    [240, 240, 100, 420],
    [240, 400, 100, 260],
    [400, 40, 100, 460],
    [400, 40, 100, 460],
    [400, 40, 100, 460],
    [400, 40, 100, 460],
    [400, 240, 100, 260],
    [400, 240, 100, 260],
    [400, 400, 100, 100],
    [400, 400, 100, 100],
    [400, 400, 100, 100],
    [400, 400, 100, 100],
]


def run(protocol: protocol_api.ProtocolContext):
    # Media reservoir definition
    phosphate = protocol.load_labware("agilent_1_reservoir_290ml",7)
    ammonia = protocol.load_labware("agilent_1_reservoir_290ml",8)
    carbon = protocol.load_labware("agilent_1_reservoir_290ml",10)
    mq = protocol.load_labware("agilent_1_reservoir_290ml",11)

    # Assay Plates
    assay_plates = [
        protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 1),
        protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 2),
        protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 5),
        protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 4)
    ]

    # Loaded Tips
    tips300 = [
        protocol.load_labware("opentrons_96_tiprack_300ul", "9")
    ]
    tips1000 = [
        protocol.load_labware("opentrons_96_tiprack_1000ul", "6")
    ]

    # Mounted Pipets
    p300Single = protocol.load_instrument("p300_single", "left", tip_racks=tips300)
    p1000 = protocol.load_instrument("p1000_single", "right", tip_racks=tips1000)

    # Pipetting
    # Phosphate
    for plate in assay_plates:
        i = 0
        p300Single.pick_up_tip()
        p1000.pick_up_tip()
        for well in plate.wells():
            if media_recipe[i][0] <= 300:
                if media_recipe[i][0] <= 50:
                    p300Single.transfer(media_recipe[i][0], phosphate["A1"], well, new_tip="never", blow_out = True, blowout_location="destination well")
                else:
                    p300Single.transfer(media_recipe[i][0], phosphate["A1"], well, new_tip="never")
            else:
                p1000.transfer(media_recipe[i][0], phosphate["A1"], well, new_tip="never")
            i += 1
        p300Single.drop_tip()
        p1000.drop_tip()

    # Ammonia
    for plate in assay_plates:
        i = 0
        p300Single.pick_up_tip()
        p1000.pick_up_tip()
        for well in plate.wells():
            if media_recipe[i][1] <= 300:
                if media_recipe[i][1] <= 50:
                    p300Single.transfer(media_recipe[i][1], ammonia["A1"], well, new_tip="never", blow_out = True, blowout_location="destination well")
                else:
                    p300Single.transfer(media_recipe[i][1], ammonia["A1"], well, new_tip="never")
            else:
                p1000.transfer(media_recipe[i][1], ammonia["A1"], well, new_tip="never")
            i += 1
        p300Single.drop_tip()
        p1000.drop_tip()

    # ddWater
    for plate in assay_plates:
        i = 0
        p300Single.pick_up_tip()
        p1000.pick_up_tip()
        for well in plate.wells():
            if media_recipe[i][3] <= 300:
                if media_recipe[i][3] <= 50:
                    p300Single.transfer(media_recipe[i][3], mq["A1"], well, new_tip="never", blow_out = True, blowout_location="destination well")
                else:
                    p300Single.transfer(media_recipe[i][3], mq["A1"], well, new_tip="never")
            else:
                p1000.transfer(media_recipe[i][3], mq["A1"], well, new_tip="never")
            i += 1
        p300Single.drop_tip()
        p1000.drop_tip()

    # Carbon
    for plate in assay_plates:
        i = 0
        p300Single.pick_up_tip()
        p1000.pick_up_tip()
        for well in plate.wells():
            if media_recipe[i][2] <= 300:
                if media_recipe[i][2] <= 50:
                    p300Single.transfer(media_recipe[i][2], carbon["A1"], well, new_tip="never", blow_out = True, blowout_location="destination well")
                else:
                    p300Single.transfer(media_recipe[i][2], carbon["A1"], well, new_tip="never")
            else:
                p1000.transfer(media_recipe[i][2], carbon["A1"], well, new_tip="never")
            i += 1
        p300Single.drop_tip()
        p1000.drop_tip()

