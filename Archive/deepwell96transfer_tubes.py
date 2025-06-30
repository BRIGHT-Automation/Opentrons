#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 09:19:01 2022

@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Transfer protocol with tubes',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for transferring a number of 96 deepwell plates into 96 PCR plate',
    'apiLevel': '2.4'
}

""" Variables"""

rows = 2 #with most it will be 8, but good to make it open for adjusting

#num of runs
num = 1

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    """ load labware """
    source_plate_1 = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location = '8')  
    dest_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', location = '9')


    """ load pipettes """
    tiprack_1 = protocol.load_labware('geb_96_tiprack_1000ul', location = '11')
    p1000 = protocol.load_instrument('p1000_single', 'left', tip_racks=[tiprack_1])

    """ liquid transfer commands """
    
    tip_placement = {1:'H1',2:'G1',3:'F1',4:'E1',5:'D1',6:'C1',7:'B1',8:'A1'}

    p1000.pick_up_tip(tiprack_1[tip_placement[rows]]) 
    p1000.aspirate(740,source_plate_1['A1'])
    for col in range(0,6):
        #130ul (10ul extra, only give 120) aspirated then dispensed over half the row, more is collected, the other half, trash
        
        p1000.dispense(120,dest_plate['A'+str(1+col)])
    p1000.return_tip()




    p1000.pick_up_tip(tiprack_1[tip_placement[rows]]) 
    p1000.aspirate(740,source_plate_1['A1'])
    for col in range(5,12):
        #130ul (10ul extra, only give 120) aspirated then dispensed over half the row, more is collected, the other half, trash
        
        p1000.dispense(120,dest_plate['A'+str(1+col)])
    p1000.return_tip()
        