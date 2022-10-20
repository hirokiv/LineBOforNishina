import os.path
import time
import gicosy.T_Cource_Transmission as TCT
import numpy as np
import sys
import shutil


class MocadiInterface:

    def __init__(self, identifier, path2Mocadi='./T_Cource_Transmission/'):
        self.identifier = identifier
        self.filename = 'MonteCarlo_Result' + self.identifier + '.txt'
        self.filepath = path2Mocadi + self.filename
        self.sleeptime = 0.05
        self.FILEMAXTD = 3
        self.lastline = 6 # last line of the output which contain ratio information
        self.transports = (7, 8) # max particles, transmitted
        self.path2Mocadi = path2Mocadi
        self.pathCurrent = os.getcwd()
        self.logfile = 'mocadiout.log'

    def RunMocadi(self, X):
        # X contains normalized scale parameter for input variables

        # output to mocadiout.log
        sys.stdout = open(self.logfile, 'a+') # temporaly set mocadiout.log as output
        try: 
            # change directory and run mocadi. 
            # return to current paht when error occurs
            os.chdir(self.path2Mocadi)
            # delete existing path file and run Mocadi
            if os.path.isfile(self.filename):
              #os.remove(self.filename)
              shutil.move(self.filename, self.filename + '_old.txt')
            

            # while statement inserted because mocadi often fails 
            # even for the same magnet value (X)
            while not (os.path.isfile(self.filename)):
                TCT.mocadi_func(self.identifier, X)
        
            # intended for asynchronous setting but seems not necessary
            # # check if the file in need is generated
            # starttime = time.time() # start time
            # if( not( os.path.isfile(self.filename) ) ):
            #     time.sleep(self.sleeptime)
            #     td = time.time() - starttime
            #     if td.second > self.FILEMAXTD:
            #       sys.exit('Mocadi failed in creating file in need')

            print('Succeeded in generating simulation results')
    
        except:
            os.chdir(self.pathCurrent)
            print('simulation_wrapper.py: Error occured. Refer X')
            print(X)
            sys.exit('Error in generating simulation result')

        finally:
            os.chdir(self.pathCurrent)
            sys.stdout = sys.__stdout__ # console output
     
    def LoadMocadiResults(self):
        # load file and check if the file generate proper output
    
        with open(self.filepath) as f:
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
    mocadi.RunMocadi()
    ratio = mocadi.LoadMocadiResults()
    print("Output : " + str(ratio) )
