#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 09:19:01 2022

@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Transfer protocol',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for transferring a number of 96 deepwell plates into 96 PCR plate',
    'apiLevel': '2.4'
}

""" Variables"""

rows = 8 #with most it will be 8, but good to make it open for adjusting

#num of runs
num = 1

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    """ load labware """
    source_plate_1 = protocol.load_labware('usascientific_12_reservoir_22ml', location = '8')  
    dest_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', location = '9')


    """ load pipettes """
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '11')
    p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1])

    """ liquid transfer commands """
    
    tip_placement = {1:'H1',2:'G1',3:'F1',4:'E1',5:'D1',6:'C1',7:'B1',8:'A1'}

    p300.pick_up_tip(tiprack_1[tip_placement[rows]]) 
    
    for col in range(12):
        #150ul from source plate with multi following the 8 rows - mixing before moving on 3 times with 150ul
        
        #p300.mix(3,120,source_plate_1['A'+str(1+col)])
        p300.aspirate(120,source_plate_1['A'+str(1+col)])
        p300.dispense(120,dest_plate['A'+str(1+col)])

    p300.return_tip()
    #p300.drop_tip()

        