import os.path
import time
from Evaluate_envelope_mocadi import mocadi_func
import numpy as np
import sys


class MocadiInterface:

    def __init__(self, identifier):
        self.identifier = identifier
        self.filename = 'MonteCarlo_Result' + self.identifier + '.txt'
        self.sleeptime = 0.05
        self.FILEMAXTD = 3
        self.lastline = 6 # last line of the output which contain ratio information
        self.transports = (7, 8) # max particles, transmitted

    def RunMocadi(self):
        # delete existing path file and run Mocadi
        if os.path.isfile(self.filename):
          os.remove(self.filename)
        
        mocadi_func(self.identifier)
    
        # check if the file in need is generated
        starttime = time.time() # start time
        if( not( os.path.isfile(self.filename) ) ):
            time.sleep(self.sleeptime)
            td = time.time() - starttime
            if td.second > self.FILEMAXTD:
              sys.exit('Mocadi failed in creating file in need')

     
    def LoadMocadiResults(self):
        # load file and check if the file generate proper output
    
        with open(self.filename) as f:
            lineiter = 0 # iterator
            for line in f.readlines():
    
                # the main output result located at the 7th line
                if lineiter == self.lastline:
                    x = np.array( line.split(",") )
                    xx = x.astype(float)
                    if len(xx) != (self.transports[1] + 1):
                        print(len(xx))
                        print(self.transports[1])
                        sys.exit('Mocadi result format wrong')
   
                    ratio = xx[self.transports[1]] / xx[self.transports[0]]
    
                # increment at the end of the line call
                lineiter += 1
    
        return ratio
    

if __name__ == '__main__':
    mocadi = MocadiInterface('_hogehoge')

    sys.stdout = open('mocadiout.log', 'a+') # temporaly set mocadiout.log as output
    mocadi.RunMocadi()
    sys.stdout = sys.__stdout__ # console output
 

    ratio = mocadi.LoadMocadiResults()
    print("Output : " + str(ratio) )
