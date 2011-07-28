#! /usr/bin/python3                                                                

#f1 = input('Plese enter name of the gro file(absolute path)\n')
#gro_file = open(f1, 'r')
gro_file = open('1qlz.gro', 'r')
H_counter = 0
O_counter = 0
C_counter = 0
N_counter = 0
S_counter = 0
atom_counter = 0

f2 = open('O_gro', 'w')
for line in gro_file:    
    if len(line) == 45:
        atom_counter += 1
        list1 = line.split()
        if list1[1].startswith('H'):
            H_counter += 1
        elif list1[1].startswith('O'):
            O_counter += 1
            f2.write('{:>3}{:>10}{}'.format(list1[1], list1[0], '\n'))
        elif list1[1].startswith('C'):
            C_counter += 1
        elif list1[1].startswith('N'):
            N_counter += 1
        elif list1[1].startswith('S'):
            S_counter += 1
        else:
            print(list1[1])

print('{:>10}{:>10}{:>10}{:>10}{:>10}'.format('H','O','C','N','S'))
print('{:>10d}{:>10d}{:>10d}{:>10d}{:>10d}'\
          .format(H_counter, O_counter, C_counter, N_counter, S_counter))
print('{} atoms'.format(H_counter + O_counter + C_counter + N_counter + S_counter))
print('{} atoms'.format(atom_counter))
print('{} non-hydrogen atoms'.format(O_counter + C_counter + N_counter + S_counter))
