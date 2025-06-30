import csv
from opentrons import protocol_api
#CSV
conjugants_csv = '''
A1;WGS65
B1;1168
C1;1391
D1;1595
A2;SGris
B2;SAlbus
C3;M1152
D3;104
A4;642
B4;859
'''

e_coli_csv = '''
A1;n9
B1;g22
C1;g17
D1;n17
A2;a14
B2;m7
'''
mixture_csv = '''
A1;WGS65;n9
B1;WGS65;g22
C1;WGS65;g17
D1;WGS65;n17
E1;WGS65;a14
F1;WGS65;m7
G1;1168;n9
H1;1168;g22
A2;1168;g17
B2;1168;n17
C2;1168;a14
D2;1168;m7
E2;1391;n9
F2;1391;g22
G2;1391;g17
H2;1391;n17
A3;1391;a14
B3;1391;m7
C3;1595;n9
D3;1595;g22
E3;1595;g17
F3;1595;n17
G3;1595;a14
H3;1595;m7
A4;SGris;n9
B4;SGris;g22
C4;SGris;g17
D4;SGris;n17
E4;SGris;a14
F4;SGris;m7
G4;SAlbus;n9
H4;SAlbus;g22
A5;SAlbus;g17
B5;SAlbus;n17
C5;SAlbus;a14
D5;SAlbus;m7
E5;M1152;n9
F5;M1152;g22
G5;M1152;g17
H5;M1152;n17
A6;M1152;a14
B6;M1152;m7
C6;104;n9
D6;104;g22
E6;104;g17
F6;104;n17
G6;104;a14
H6;104;m7
A7;642;n9
B7;642;g22
C7;642;g17
D7;642;n17
E7;642;a14
F7;642;m7
G7;859;n9
H7;859;g22
A8;859;g17
B8;859;n17
C8;859;a14
D8;859;m7
'''

# metadata
metadata = {
    'protocolName': 'Conjugation v 0.0.2',
    'author': 'Thom Booth <thoboo@biosustain.dtu.dk>',
    'description': 'Protocol for transformation of Streptomcyes spores by conjugation with E.coli',
    'apiLevel': '2.12'
}

def read_csv(csv_input):
    rows = []
    csv_data = csv_input.splitlines()[1:]
    csv_reader = csv.reader(csv_data)
    rows = []
    for row in csv_reader:
        print(row)
        rows.append(row[0].split(';'))
    return rows 
    

def get_order_of_operations():
    conjugants = read_csv(conjugants_csv)
    e_colis = read_csv(e_coli_csv)
    mixture = read_csv(mixture_csv)
    e_coli_coordinates = []
    conjugant_coordinates = []
    mixture_coordinates = []
    for line in mixture:
        e_coli_position = [e_coli[0] for e_coli in e_colis if e_coli[1] == line[2]]
        e_coli_coordinates.extend(e_coli_position)
        conjuagant_position = [conjugant[0] for conjugant in conjugants if conjugant[1] == line[1]]
        conjugant_coordinates.extend(conjuagant_position)
        mixture_coordinates.append(line[0])
    return e_coli_coordinates, conjugant_coordinates, mixture_coordinates

def get_string(list_):
    string_ = ''.join([str(item) for item in list_])

def run(protocol: protocol_api.ProtocolContext):
    #labware -----update
    conjugant_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')
    e_coli_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '1')
    mixture_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '3')
    tiprack_1000 = protocol.load_labware('geb_96_tiprack_1000ul', '4')
    #pippettes
    right_pipette = protocol.load_instrument('p1000_single', 'left', tip_racks=[tiprack_1000])
    #get operations from file
    e_coli_coordinates, conjugant_coordinates, mixture_coordinates = get_order_of_operations()
    #run commands
    #transfer e_coli
    for e_coli in set(e_coli_coordinates):
        right_pipette.pick_up_tip()
        for i in range(0,len(e_coli_coordinates)):
            if e_coli_coordinates[i] == e_coli:
                right_pipette.aspirate(100, e_coli_plate[e_coli])
                right_pipette.dispense(100, mixture_plate[mixture_coordinates[i]])
                right_pipette.blow_out()
        right_pipette.drop_tip()
    #transfer conjugants
    for conjugant in set(conjugant_coordinates):
        right_pipette.pick_up_tip()
        for i in range(0,len(conjugant_coordinates)):
            if conjugant_coordinates[i] == conjugant:
                right_pipette.mix(4, 100,conjugant_plate[conjugant])
                right_pipette.aspirate(100, conjugant_plate[conjugant].bottom(+2))
                right_pipette.dispense(100, mixture_plate[mixture_coordinates[i]].top(-2))
                right_pipette.blow_out()
        right_pipette.drop_tip()

    