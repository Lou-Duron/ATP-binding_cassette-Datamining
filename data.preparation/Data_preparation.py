#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import argparse

################################################################################################
parser = argparse.ArgumentParser(description='Data preparation')
parser.add_argument('--user', '-u', type=str, help="username for the database")
parser.add_argument('--password', '-p', type=str, help="passsword for the database")
parser.add_argument('--score', '-s', type=int, default=int(30), help="minimal score for domain recovery, default = 30")
parser.add_argument('--nb_domain', '-n', type=int, default=int(10), help="minimal number of occurence in gene dataset of each domains, default = 10")
parser.add_argument('--abc', '-a', required=False, action="store_true", help='return a csv file with the matrix for abc gene detection')
parser.add_argument('--sub', '-b', required=False, action="store_true", help='return a csv file with the matrix for abc subtype detection')
'''
Example of use: ./Data_parser.py -u user -p pwd -s 40 -n 10 -a -b
It will keep only conserved domains having a score > 40 that appears in at least 10 genes
With this setting this parser will create 2 csv file :
- abc.csv : for the prediction abc-type genes
- subfamilies.csv : for the prediction of abc subfamilies
'''
args = parser.parse_args()
################################################################################################

# Connexion to the database
conn = mc.connect(host = 'localhost',
database = 'fouille',
user = args.user,
password= args.password)
cursor = conn.cursor()

# Recovery of abc-type protein sub-type (class)
cursor.execute("SELECT Gene_ID, Type, Identification_Status, Domain_Structure FROM Protein")
cl = {} # cl = {Gene_ID : class} 0 : MSD, 1 : NBD, 2 : SBP, 3 : multiple
for el in cursor:
    if el[1] == "ABC" and el[2] == "Confirmed":
        if(el[3] == "MSD"):
            cl[el[0]] = 0
        elif(el[3] == "NBD"):
            cl[el[0]] = 1
        elif(el[3] == "SBP"):
            cl[el[0]] = 2
        else:
            cl[el[0]] = 3

# Recovery of abc-subtype specific domains
cursor.execute("SELECT Gene_ID, Score, FD_ID FROM Conserved_Domain")
sub = {} # sub = {class : [associated_domains]}
temp = {}
for el in cursor:
    if(el[1] > args.score):
        if(el[0] in cl.keys()):
            if(cl[el[0]] not in sub.keys()):
                sub[cl[el[0]]] = []
                temp[cl[el[0]]] = {}
            if(el[2] not in temp[cl[el[0]]].keys()):
                temp[cl[el[0]]][el[2]] = 1
            else:
                temp[cl[el[0]]][el[2]] += 1
for cla in temp.keys():
    for fd in temp[cla]:
        if(temp[cla][fd] > args.nb_domain):
            sub[cla].append(fd)

# Recovery of number of domains
cursor.execute("SELECT Gene_ID, FD_ID FROM Conserved_Domain")
nb = {} # nb = {Gene_ID : [nb_MSD_domains, nb_NBD_domains, nb_SBP_domains]}
for el in cursor:
    if(el[0] not in nb.keys()):
        nb[el[0]] = [0,0,0]
    if(el[1] in sub[0]):
        nb[el[0]][0] += 1
    elif(el[1] in sub[1]):
        nb[el[0]][1] += 1
    elif(el[1] in sub[2]):
        nb[el[0]][2] += 1


# Creation of csv files
# abc.csv file
if args.abc:
    with open("abc.csv", "w") as abc:
        abc.write("class,Gene_ID,Length,MSD_associated_domains,NMD_associated_domains,SBP_associated_domains"+"\n")
        cursor.execute("SELECT Gene_ID, abs(End-Start) FROM Gene")
        for el in cursor:
            if(el[0] in cl.keys()):
                abc.write("1, ") 
            else:
                abc.write("0, ")
            abc.write(str(el[0]) + ", " + str(el[1]) + ", ")
            if(el[0] in nb.keys()):
                abc.write(str(nb[el[0]][0]) + ", " + str(nb[el[0]][1]) + ", " + str(nb[el[0]][2]))
            else:
                abc.write("0, 0, 0")
            abc.write("\n")

# subfamilies.csv file
if args.sub:
    with open("subfamilies.csv", "w") as sub:
        sub.write("class,Gene_ID,Length,MSD_associated_domains,NMD_associated_domains,SBP_associated_domains"+"\n")
        cursor.execute("SELECT Gene_ID, abs(End-Start) FROM Gene")
        for el in cursor:
            if(el[0] in cl.keys() and el[0] in nb.keys()):
                sub.write(str(cl[el[0]]) + ", ")
                sub.write(str(el[0]) + ", " + str(el[1]) + ", ")
                if(el[0] in nb.keys()):
                    sub.write(str(nb[el[0]][0]) + ", " + str(nb[el[0]][1]) + ", " + str(nb[el[0]][2]))
                sub.write("\n")


