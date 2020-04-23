from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.  
    # You use equation B to get the desired phi from P and d
    # You then use equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = 1 - maxFalsePositive**(1/numHashes)
        return numHashes/(1-(phi)**(1/numKeys))
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__numBitsSet= 0  # numBitsSet counter
        self.__bitVector = BitVector(size=int(self.__bitsNeeded(numKeys, numHashes, maxFalsePositive))) #create a bitVector
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        n = 0                                                         #initialize n to 0
        for i in range(self.__numHashes):                             #loop through hash
            n = BitHash(key, n)                                       #now n is the new hash
            if self.__bitVector[n%len(self.__bitVector)] == 0:        #increment count of set bits if it wasnt 1.    
                self.__numBitsSet +=1
            self.__bitVector[n%len(self.__bitVector)] = 1 
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        n = 0
        for i in range(self.__numHashes):
            n = BitHash(key, n)
            if self.__bitVector[n%len(self.__bitVector)] != 1:        #stop looping if is not one
                return False
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        phi = (len(self.__bitVector) - self.__numBitsSet)/len(self.__bitVector)
        return (1 - phi)**self.__numHashes
        
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numBitsSet


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fin = open("wordlist.txt")
    for i in range(numKeys):
        b.insert(fin.readline())
    fin.close()    
    
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("Projected false positive rate: ", b.falsePositiveRate())
    
    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    fin = open("wordlist.txt")
    count = 0
    for i in range(numKeys):
        if not b.find(fin.readline()):
            count +=1
    print(count)
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    falselyFound = 0
    for i in range(numKeys):
        if b.find(fin.readline()):
            falselyFound +=1
    fin.close()
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    
    print("False positives rate:", falselyFound/numKeys)
    

    
if __name__ == '__main__':
    __main()       

