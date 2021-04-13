# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:07:34 2021

@author: Oliver Hong
"""

import enchant
import random as r
import math 

d = enchant.Dict("en_US")

#generates a random sequence of words with certain rules
def random_sequence (sequence_length):
    sequence = ""
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',\
                  's', 't', 'v', 'w', 'x', 'z']
    length = 0 #tracks length of sequence
    space = 0 #used to prevent two spaces in a row
    word_type = 0 #increases chances of vowels after consonants and vice versa
    consonant_frequency = 77
    space_frequency = 15
    
    contains_space = True
    
    while length < sequence_length and contains_space:
        n = r.randint(0,100)
        word_type_gen = r.randint (0,10)
        if n > space_frequency or space == 1: #n is the rng to decide space frequency
            m = r.randint(0,100) #m is rng to decide consonant vs vowel
            
            if word_type == 1 and word_type_gen < consonant_frequency:
                sequence = sequence + r.choice(consonants)
                word_type = 0 #if consonant is added, word_type = 0 
            elif m < consonant_frequency:
                sequence = sequence + r.choice(consonants)
                word_type = 0 #if consonant is added, word_type = 0
            else:
                sequence = sequence + r.choice(vowels)
                word_type = 1 #if vowel is added, word_type = 1
                
            length += 1
            space = 0
            
        elif space != 1:
            sequence = sequence + " "
            length += 1
            space = 1
            
    #Makes sure that random_sequence doesnt output " " for 1 long sequences.
    if sequence != " ":
        contains_space = False
                
    return sequence

#Uses random_sequence to generate random "words" and splits them into 2 word chunks. 
#Chunks are kept if at least one word in the chunk is "correct".
#s_length specifies how long the total input sequence is
#o_length specifies criteria for how long a word must be to be correct excluding I and a.
def selection (s_length, o_length):

    output_smaller_than_0 = True
    #Runs loop to select "correct" words from random sequence until output is not blank
    #random sequence sometimes does not generate any "correct words" and the organism's DNA will 
    #be blank, which is bad later on.
    while output_smaller_than_0:
        span = 1 
        #change chunk size (span = 1 means all selection outputs are words)
        #span = 2 means chunks are two words long and at least one needs to be correct to be outputted.
        seq = random_sequence(s_length)
        check = seq.split()
        check = [" ".join(check[i:i+span]) for i in range(0, len(check), span)]
        output = ""
        
        for i in check:
            piece = i.split()
            group_length = len(piece)
            if group_length == 2: 
                if d.check(piece[0]) == True or d.check(piece[1]) == True:
                    if len(piece[0]) > o_length and len(piece[1]) > o_length and i != " " \
                    or i == "i" or i == "a":
                        output = output + piece[0] + " " + piece[1] + " "
            elif group_length == 1:
                if d.check(piece[0]) == True:
                    if len(piece[0]) > o_length\
                    and piece[0] != " " or i == "i" or i == "a":
                        output = output + piece[0] + " "
        
        output = S_endonuclease("i a", output)
        output_smaller_than_0 = len(output) < 2

    return output

#Part of a class of "endonucleases" that cuts out certain (extraneous) sequences
#from dictionary values (D)
def D_endonuclease(prune_sequence, dictionary):
    for k, v in dictionary.items():
        output = ""
        for i in v.split():
            if i not in prune_sequence.split():
                output = output + i + " "
        dictionary[k] = output
    return dictionary

#Endonuclease that cuts out certain (extraneous) sequences from strings
def S_endonuclease(prune_sequence, string):
    output = ""
    for s in string.split():
        if s not in prune_sequence.split(): #checks if individual word is in prune criteria
            output = output + s + " "
    return output
        

Species = {}

letter_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',\
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
#Creates primordial species A-Z, 
def create_primordial():
    Species1 = {}
    a = 0
    t = 0
    while t < (26):
        DNA = selection(1000, 2) 
        species_tag = "/1/" + str(letter_code[a])
        Species1.update({species_tag: DNA})
        a += 1
        t += 1
    return Species1

#Function that simulates a "low fidelity" polymerase class enzyme 
#and natural selection/population fitness and growth.
def replication(dictionary):
    survival = 0.5 #minimum value of growth fitness for species to not go extinct
                   #Do not set as negative since that does some funny stuff
    allee_effect = 0.45 #Above 0 to below 1
                       #Percent of average species population needed to reproduce.
    capacity = 1000000 #Carrying capacity for the specific species 
                      #(set it high or all species just go extinct)
    a = 0
    b = 0
    temp_dictionary = {}
    total_population = 0
    
    #For loop to add individual populations of species together to get total population
    for k in dictionary.keys():
        decode1 = k.split("/") #Decodes the /pop/ prefix
        total_population += int(decode1[1]) #Extracts the population value and calculates total
   
    #Main replication loop
    for k, v in dictionary.items():

        replication = ""
        mutated = 0
        if r.randint(0,100) < 50: #50% of replications result in some type of mutation
            mutated = 1 #variable identifies whether current iteration is mutated or not since a
                        #different naming scheme is used between mutated and conserved.
                        
            new_species_tag = str(letter_code[a]) #Alphabetical naming system
            replication = v + " " #moves values that will be mutated to another variable
            
            #End addition mutation (lengthening)
            if r.randint(0,100) < 50: 
                replication = replication + selection(10000, 3)
                
            #Subsitution Mutation
            elif r.randint(0,100) < 50: 
                split = replication.split()
                split[r.randint(0, (len(split) - 1))] = random_sequence(r.randint(0,20))
                replication = ""
                for i in split:
                    replication = replication + i + " "
            #Insertion Mutation  
            else: 
                split = replication.split()
                split.insert(r.randint(0, (len(split) - 1)), random_sequence(r.randint(0,20)))
                replication = ""
                for i in split:
                    replication = replication + i + " "

            b += 1 #Incrementer for naming system
            if b > 8:
                b = 0
                a += 1

        decode = k.split("/") #Decodes the /pop/ prefix
        population = int(decode[1]) #Extracts the population value
        
        #If not mutated, population fitness is modelled with non-mutated values.
        if mutated == 0: 
            #Evaluates "fitness" of non-mutated species by # of correct words and # of long words
            check1 = v.split()
            x1 = 0 #counts correct words
            y1 = 0 #counts correct words with length > 3 and adds the length of that word, not 1.
            for i in check1:
                if d.check(i) == True:
                    x1 += 1
                    if len(i) > 3:
                        y1 += len(i)
                        
            if len(check1) > 0 and population > (allee_effect*(total_population/len(dictionary))):
                fitness1 = (x1+y1)/len(check1)
                modify = k.split("/")
                #Calculates growth rate with logistic population growth model
                #If total population exceeds capacity, then rate will be negative
                growth_rate1 = (population*((fitness1**2)*((capacity - total_population)/capacity)))
                if population + growth_rate1 > 0 and fitness1 > survival:
                    temp_dictionary.update({"/" + str(math.ceil(population + growth_rate1))\
                    + "/" + modify[-1]: v}) 
                    #grows at full rate since both strands are non-mutation fixed
        #If mutated, population fitness is calculated for the original and mutated
        #species to accurately model when a mutation is beneficial or not.
        elif mutated == 1:
            #Evaluates "fitness" of species by # of correct words and # of long words
            check1 = v.split()
            x1 = 0 #counts correct words
            y1 = 0 #counts correct words with length > 3 and adds the length of that word, not 1.
            for i in check1:
                if d.check(i) == True:
                    x1 += 1
                    if len(i) > 3:
                        y1 += len(i)
                        
            check2 = replication.split()
            x2 = 0 #counts correct words
            y2 = 0 #counts correct words with length > 3 and adds the length of that word, not 1.
            for i in check2:
                if d.check(i) == True:
                    x2 += 1
                    if len(i) > 3:
                        y2 += len(i)
                        
            if len(check2) > 0 and population > (allee_effect*(total_population/len(dictionary))):
                fitness1 = (x1+y1)/len(check1)
                fitness2 = (x2+y2)/len(check2) 
                modify = k.split("/")
                growth_rate1 = (population*((fitness1**2)*((capacity-total_population)/capacity)))
                growth_rate2 = (population*((fitness2**2)*((capacity-total_population)/capacity)))
                
                if population + growth_rate2 > 0 and fitness2 > survival:
                    temp_dictionary.update({"/" + str(math.ceil(population + 0.5*growth_rate2))\
                    + "/" + modify[-1] + "-" + new_species_tag + str(b): replication})  
                    #replicated (fixed mutation) strand (grows at half rate)
                        
                    temp_dictionary.update({"/" + str(math.ceil(population + 0.5*growth_rate1))\
                    + "/" + modify[-1]: v}) #parent strand (grows at half rate)

    return temp_dictionary
                    
Species = create_primordial()
#Always prune after Species = Species1 and not before
Prune = D_endonuclease("i a", Species)
replicated = replication(Prune)

counter = 3
t = 0
while t < counter:
    print("Generation: ", str(t))
    replicated = replication(replicated)
    replicated = D_endonuclease("i a", replicated)
    [print(key, ":", value) for key, value in replicated.items()]

    t += 1
    


