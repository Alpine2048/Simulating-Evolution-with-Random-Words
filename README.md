# Simulating-Evolution-with-Random-Words
A monke on a keyboard given sufficient time will eventually write the entire works of Shakespeare. A cellular organism given sufficient resources and time will eventually give rise to monke.

Actual (not meme) Description:

Program generates random sequences of letters and spaces according to some preset frequencies (consonants at x frequency and spaces at y frequency). These sequences of "DNA" are assigned to a "species" in a dictionary (key = species tag, value = DNA). This is done 26 times to generate one primordial species named from A-Z. After some minor clean up functions and small modifications to the dictionary, a new generation is started. What this means is that the "DNA" undergoes a low fidelity replication, with a high chance of mutations (so far there are lengthening, subsitution, and insertion mutations), which are sequences of words from the random letter generator. Following this, the DNA is evaluated to derive a "fitness" value which correlates how fit a species is to the percentage of correct words there are in it's DNA (biased such that longer correct words are more fit). This fitness is then used to calculate the growth rate of the organism using a logistic model. Thus, generation after generation, mutations occur and "fit" species grow in numbers, while those that cannot keep a reasonable population/be fit enough go extinct and are not retained in the dictionary.

The output format looks something like this:

Generation: #(starting from 0)
/#/A-A0-B1 :  blah blah blah continued
.
/#/F-C3 :  bleh blah bleh maybe
.
/#/Z-Z8-Z5 :  red fox hjk gob

The number in the / / is the population of that species. The sequence of letters and numbers after that is the species tag, or the name persay. Then you get the "DNA" sequence.
With the species tag, one can construct a phylogeny where a one mutation difference results in two species (this is an assumption). The first letter tells you which primordial species this species originated from, but the letter# sequences after are not related at all to the primordial species and just serve as "names" assigned to the mutation that speciated it.

Ex: S-S2-E2 | This is a S species that had two mutations (S2 and E2) that gave rise to the current species. The S2 mutation here would not be the same S2 mutation referred to b             | by E-S2 for example, but would be the same for all S primordial originated species.
    S       | This is the primordial species that has supposedly not gone extinct and survives
    S-S2-D3 | This species has a common ancestor (S-S2) with S-S2-E2. 
    S-S1    | This species originated through a mutation of the primordial S species.

The phylogenetic tree would look something like this:


        S  
    /       \
  S-S1     S-S2
  |       /    \
  |      S-S2  S-S2
  S-S1   -D3   -E2


 WIP stuff:
 - Extinction events based on frequency-magnitude relationship (less severe "extinctions" or selective pressures occur less frequently, and likewise)
 - Changing naming system from current system to a system that reflect the type of mutation that occured (letter) and a unique identifier (to seperate it from others) as a number sequence.
 - Interactive stats: (Total biomass per gen, most fit species per gen, average fitness of each generation, etc.)
 - Mating/conjugation: Some form of interaction between subspecies that would allow exchange of words unique to each parent. Requires redefining what a species is (no longer one mutation difference).
 - Optimization: Code right now is a ferrari built out of concrete, meant to run fast, but clunky and heavy. Needs to be optimized for speed so that >1000 generation simulations are reasonable
 - Debugging: always needed and always painful.
    
    
