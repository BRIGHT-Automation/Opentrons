metadata = {
    'protocolName': 'Coco - circular plating 1-48',
    'fileName': 'transfPlating_circular_1.py',
    'author': 'Jaime',
    'source': 'DTU Biosustain',
    'apiLevel': '2.11'
}


import math
from opentrons import types

#from opentrons.protocol_api.labware import load_from_definition
#import json

#with open('thermoscientificnunc_8_wellplate_12000ul.json') as f:
#    custom_def = json.load(f)


def run(protocol):
    # ---------- CONFIG ----------
    well_count = 48                  # number of wells in this run (0-47)
    plating_volume = 50             # total µL to dispense for each sample
    plate_format = 8                # each Omnitray has 8 wells
    num_rings = 4                   # number of concentric rings
    total_points = 10               # total spots (including center)

    # ---------- LOAD PIPETTE + TIPRACK  + PLATES----------
    tips20 = [protocol.load_labware('opentrons_96_filtertiprack_200ul', '9')]
    p20 = protocol.load_instrument('p300_single', 'right', tip_racks=tips20)

    plate_type = "thermoscientificnunc_8_wellplate_12000ul"
    tray_slots = [1, 2, 3, 4, 5, 6]  # 6 Omnitrays -> total 6*8 = 48 wells
    agar_plates = [
        protocol.load_labware(plate_type, slot, label=f"Omnitray_{i+1}")
        for i, slot in enumerate(tray_slots)
    ]

    cell_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", '7')

    # ---------- HELPER FUNCTIONS ----------
    def degrees_to_radians(deg):
        return deg * math.pi / 180

    def distribute_points_uniformly(total_radius, points_count, ring_count):
        """
        Returns a list of (x, y) coordinates. One center point plus ring_count
        rings' worth of points, all spaced uniformly.
        """
        points = [(0, 0)]  # always add center first
        # total circumference across all rings
        total_circum = sum(
            2 * math.pi * total_radius * (ring / ring_count)
            for ring in range(1, ring_count + 1)
        )
        points_per_length = points_count / total_circum

        def add_points_on_ring(r, n):
            angle_incr = 360 / n
            for i in range(n):
                theta = degrees_to_radians(i * angle_incr)
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                points.append((x, y))

        for ring_idx in range(1, ring_count + 1):
            ring_r = total_radius * ring_idx / ring_count
            ring_circ = 2 * math.pi * ring_r
            n_points = int(round(points_per_length * ring_circ))
            add_points_on_ring(ring_r, max(n_points, 1))

        return points

    def calculate_plate(well_index):
        """Which tray index to use based on 8 wells/tray."""
        return well_index // plate_format

    def calculate_well(well_index):
        """Which well index on a single tray (0–7)."""
        return well_index % plate_format

    def spot(pipette, dest, coords, total_vol):
        """
        Takes a pipette, destination well, coordinate list, and total volume.
        Dispenses total_vol across those coords inside the well.
        """
        dispense_rate = 0.2  # slower to avoid splashing
        vol_per_point = total_vol / len(coords)

        for (x, y) in coords:
            safe = dest.bottom(z=6).move(types.Point(x=x, y=y, z=4))
            target = dest.bottom(z=6).move(types.Point(x=x, y=y, z=0))
            pipette.move_to(safe)
            protocol.max_speeds['Z'] = 50
            pipette.move_to(target)
            pipette.dispense(vol_per_point, rate=dispense_rate)
            pipette.move_to(target)
            pipette.move_to(safe)
            del protocol.max_speeds['Z']

    # ---------- PRE-COMPUTE THE SPOT PATTERN ----------
    # We'll take the diameter from the first well "A1" in the first tray
    # subtracting 3 mm from radius to avoid edges
    # Let's fetch width and length (both in mm) from the labware
    well_width = agar_plates[0]['A1'].width
    well_length = agar_plates[0]['A1'].length

    # Decide a "circular radius" that fits
    # For a circle that definitely fits inside the rectangle, use half the smaller dimension
    bounding_circle_radius = min(well_width, well_length) / 2

    # Maybe subtract 3 mm to avoid edges
    well_radius = bounding_circle_radius - 5
    circle_points = distribute_points_uniformly(
        total_radius=well_radius,
        points_count=total_points,
        ring_count=num_rings
    )

    # ---------- PLATE FUNCTION ----------
    def plate(well_index, vol):
        """For a single sample well_index, pick up tip, aspirate, and spot in rings."""
        src = well_index  
        dest_plate_idx = calculate_plate(src)
        dest_well_idx = calculate_well(src)

        p20.pick_up_tip(tips20[0].wells()[src])
        # Mix in the source well
        p20.mix(3, vol, cell_plate.wells()[src], rate = 0.3)
        # Aspirate from the source
        p20.aspirate(vol, cell_plate.wells()[src], rate=0.1)
        # Perform circular spotting in the correct tray well
        depth = agar_plates[dest_plate_idx].wells()[dest_well_idx].bottom(z=6)
        spot(p20, agar_plates[dest_plate_idx].wells()[dest_well_idx], circle_points, vol)
        p20.blow_out(depth)
        # Drop the tip
        p20.drop_tip()

    # ---------- MAIN LOOP (WELLS 0–48) ----------
    for w in range(well_count):
        plate(w, plating_volume)