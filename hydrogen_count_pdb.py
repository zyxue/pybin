#! /usr/bin/python3                                                            

#f1 = input('Plese enter name of the pdb file(absolute path)\n')
pdb_file = open('1QLZ.pdb', 'r')
H_counter = 0
O_counter = 0
C_counter = 0
N_counter = 0
S_counter = 0
atom_counter = 0

f2 = open('O_pdb', 'w')
for line in pdb_file:
    if line.startswith('ATOM'):
        atom_counter += 1
        list1 = line.split()
        if list1[-1] == 'H':
           H_counter += 1 
        elif list1[-1] == 'O':
            O_counter += 1
            f2.write('{:>5}{:>3}{:>6}{}'.format(list1[1], list1[2], list1[3], '\n'))
        elif list1[-1] == 'C':
            C_counter += 1
        elif list1[-1] == 'N':
            N_counter += 1
        elif list1[-1] == 'S':
            S_counter += 1
        else:
            print(list1[-1])
    elif line.startswith('TER'):
        break

print('{:>10}{:>10}{:>10}{:>10}{:>10}'.format('H','O','C','N','S'))
print('{:>10d}{:>10d}{:>10d}{:>10d}{:>10d}'\
          .format(H_counter, O_counter, C_counter, N_counter, S_counter))
print('{} atoms'.format(H_counter + O_counter + C_counter + N_counter + S_counter))
print('{} atoms'.format(atom_counter))
print('{} non-hydrogen atoms'.format(O_counter + C_counter + N_counter + S_counter))
