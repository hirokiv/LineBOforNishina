import os.path
import time
#import __init__ as TCT
import numpy as np
import sys
import shutil
import re

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# import T_Cource_Transmission as TCT
# import ElectroMagnetConfig
import gicosy.T_Cource_Transmission as TCT
import gicosy.ElectroMagnetConfig


class MocadiInterface:

    def __init__(self, identifier, path2Mocadi='./T_Cource_Transmission/', BQConfig=None):
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

        # register normalization factors for BQ
        self.registerBQConfig(BQConfig)

        # define the maximum particle ratio each wall can accept
        self.num_constraints = 30
        self.ratio_constraints = 0.12
        self.damage_threshold = self.ratio_constraints * np.ones(self.num_constraints, dtype = "float32")

    def registerBQConfig(self, BQConfig):
        self.BQConfig = BQConfig

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
                TCT.mocadi_func(self.identifier, X, self.BQConfig)
        
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

            # initialize lost particles readouts
            lostparticles = []

            for line in f.readlines():

                

                # above 5 lines indicates constraints
                # first element contains label (ex. Dipole#0 in:)
                if lineiter < self.lastline:
                    x = np.array( re.split(r'[:,]', line) )
                    xx = x[1:].astype(float)
                    lostparticles = np.hstack((lostparticles, xx))

    
                # the main output result (transmitted particles) located at the 7th line
                if lineiter == self.lastline:
                    x = np.array( line.split(",") )
                    xx = x.astype(float)
                    if len(xx) != (self.transports[1] + 1):
                        print(len(xx))
                        print(self.transports[1])
                        sys.exit('Mocadi result format wrong')
   
                    transported = xx[self.transports[1]]
                    initial_num = xx[self.transports[0]]
                    ratio = transported / initial_num
    
                # increment at the end of the line call
                lineiter += 1


        # normalize lost particles at each obstacle by the total num of particles
        self.lost = lostparticles / initial_num 
    
        return ratio

    def LoadConstraint(self, n):
        # n indicates the indice of the constraints nmax>=n>=1
        # constraints contained in 6x5 matrices (except string at the head)
        rows = 6
        cols = 5

        irows = n // rows
        icols = (n-1) % cols

        with open(self.filepath) as f:
            lineiter = 0 # iterator

            # initialize lost particles readouts
            lostparticles = []

            for line in f.readlines():
                # above 5 lines indicates constraints
                # first element contains label (ex. Dipole#0 in:)
                if lineiter == irows:
                    x = np.array( re.split(r'[:,]', line) )
                    xx = x[1:].astype(float)
                    lostparticles = np.hstack((lostparticles, xx))
                # the main output result (transmitted particles) located at the 7th line
                if lineiter == self.lastline:
                    x = np.array( line.split(",") )
                    xx = x.astype(float)
                    if len(xx) != (self.transports[1] + 1):
                        print(len(xx))
                        print(self.transports[1])
                        sys.exit('Mocadi result format wrong')
   
                    initial_num = xx[self.transports[0]]
    
                # increment at the end of the line call
                lineiter += 1
    
        return lostparticles[icols] / initial_num


# Prepare constraint functions which just read num of particles from the file
mocadi_const = MocadiInterface('__environment', 'gicosy/T_Cource_Transmission/')
def MocadiConstraint(n): # X is augmented augument to be consistent with benchmarks.py
    lost = mocadi_const.LoadConstraint(n)
    return (lost - mocadi_const.damage_threshold[n-1]) / mocadi_const.damage_threshold[n-1]

def MocadiConstraint1(X=None):
    return MocadiConstraint(1)
def MocadiConstraint2(X=None):
    return MocadiConstraint(2)
def MocadiConstraint3(X=None):
    return MocadiConstraint(3)
def MocadiConstraint4(X=None):
    return MocadiConstraint(4)
def MocadiConstraint5(X=None):
    return MocadiConstraint(5)
def MocadiConstraint6(X=None):
    return MocadiConstraint(6)
def MocadiConstraint7(X=None):
    return MocadiConstraint(7)
def MocadiConstraint8(X=None):
    return MocadiConstraint(8)
def MocadiConstraint9(X=None):
    return MocadiConstraint(9)
def MocadiConstraint10(X=None):
    return MocadiConstraint(10)
def MocadiConstraint11(X=None):
    return MocadiConstraint(11)
def MocadiConstraint12(X=None):
    return MocadiConstraint(12)
def MocadiConstraint13(X=None):
    return MocadiConstraint(13)
def MocadiConstraint14(X=None):
    return MocadiConstraint(14)
def MocadiConstraint15(X=None):
    return MocadiConstraint(15)
def MocadiConstraint16(X=None):
    return MocadiConstraint(16)
def MocadiConstraint17(X=None):
    return MocadiConstraint(17)
def MocadiConstraint18(X=None):
    return MocadiConstraint(18)
def MocadiConstraint19(X=None):
    return MocadiConstraint(19)
def MocadiConstraint20(X=None):
    return MocadiConstraint(20)
def MocadiConstraint21(X=None):
    return MocadiConstraint(21)
def MocadiConstraint22(X=None):
    return MocadiConstraint(22)
def MocadiConstraint23(X=None):
    return MocadiConstraint(23)
def MocadiConstraint24(X=None):
    return MocadiConstraint(24)
def MocadiConstraint25(X=None):
    return MocadiConstraint(25)
def MocadiConstraint26(X=None):
    return MocadiConstraint(26)
def MocadiConstraint27(X=None):
    return MocadiConstraint(27)
def MocadiConstraint28(X=None):
    return MocadiConstraint(28)
def MocadiConstraint29(X=None):
    return MocadiConstraint(29)
def MocadiConstraint30(X=None):
    return MocadiConstraint(30)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# def MocadiConstraint1(X=None):
#     return MocadiConstraint(1)
# 


# prepared to add path to the save path, but no longer needed
# def p_re(path, string):
#     # replace path to the directory containting T_Course_Transmission 
#     # specify as ./~
#     if not (type(path) is str):
#         sys.exit('Wrapper path error in Evaluate_Envelope_Mocadi.py')
#     if path[-1] != '/':
#         path += '/'
#     return string.replace("./", "./" + path)

# initial BQ values (hard-coded)
class ElectroMagnetConfig:
    def __init__(self):
        self.BQ0 = np.atleast_2d([
            -3.58757E-01,
            -8.50502E-03,
            0.180925008,
            0.265975226,
            -0.0,
            -0.00136544,
            0.044999297,
            0.364942752,
            -0.42834382,
            -0.4391684,
            0.34020087,
            -0.29690258,
            0.53968229,
            -0.25515065,
            0.740710077,
            -0.6154543,
            0.511847673    
        ]) # initialize as 2d array
    
        # note for later restricting the input value
        self.polarity = np.atleast_2d([
           -1,-1,+1,+1,
            -1,-1,+1,
            +1,-1,
            -1,+1,
            -1,+1,-1,
            +1,-1,+1
        ])

        # Following factors are factors for normalized variation between (-1,1)
        #tempBQ0 = self.BQ0
        #tempBQ0[0][4] = 0 # just to augment by multiplication factor
        #self.BQ0_factor = tempBQ0 * 0.2 # set to \pm 10%
        # normalize X0 based on polarity
        self.setBQRange()
        self.ConvertBQ0_to_X0()
  
        self.BQ = None

    def ConvertBQ0_to_X0(self):
        # convert BQ0 to X based on max and min range
        self.X0 = (self.BQ0 - self.BQave) / (self.BQ_factor + 1e-20) # avoid 0 division
        print('###############################')
        print('show X0')
        print('###############################')
        print(self.X0)
        # print(self.BQ0)
        # print(self.BQave)
        # print(self.BQ_factor)

    def getX0(self):
        return self.X0

    def setBQRange(self):
        # temporaly based on polarity and 1 maximum
        print('setBQRange called')
        BQ0_multiplied = np.abs(self.BQ0 * 1.5) # allow 1.5 times multiple for each
        self.BQmax = BQ0_multiplied * (np.atleast_2d([0 if i<0 else i for i in self.polarity.flatten()]))
        self.BQmin = BQ0_multiplied * (np.atleast_2d([0 if i>0 else i for i in self.polarity.flatten()]))
        self.BQave = (self.BQmax + self.BQmin) / 2.
        self.BQ_factor = self.BQmax - self.BQave
        print('###############################')
        print('show max and min')
        print('###############################')
        print(self.BQmax)
        print(self.BQmin)
        print(self.BQave)
        print(self.BQ_factor)

    def setBQ(self, X):
        # set BQ based on X each dimension normalized by BQmax and BQmin.
        # X should take range between -1 to 1
        if self.BQ0.shape != X.shape:
            sys.exit('BQ set error')
        self.BQ = self.BQave + self.BQ_factor * ( X )
        return self.BQ

    def getBQ(self):
        if (self.BQ == None).all() or (self.BQ.shape != self.BQ0.shape):
            sys.exit('BQ set error')

        print('#########################################################')
        print('## Evaluate_Envelope_mocadi.py getBQ ##')
        print(self.BQ.flatten())
        print('#########################################################')

        return self.BQ.flatten()

    def getBQ0(self):
        return self.BQ0.flatten()

    def getPolarity(self):
        return self.polarity.flatten()

 

if __name__ == '__main__':

    dim = 17
    sweep_dim = 17 # prepared 4 multiples
    #X0 = np.atleast_2d( np.zeros(dim) )
    X_1d = np.linspace(-1, 1, sweep_dim)
    Y = np.zeros( (dim, sweep_dim) )

    # loop until error occurs

    BQConfig = ElectroMagnetConfig()
    X0 = BQConfig.getX0()
    mocadi = MocadiInterface('_hogehoge', './', BQConfig)

    print(X0)
    mocadi.BQConfig.setBQ(X0)
    print(mocadi.BQConfig.getBQ())


    for idx in range(dim):

        for idx_1d in range(len(X_1d)):
            X = X0.copy()
            X[0][idx] = X_1d[idx_1d]
            print(X)
    
            if os.path.isfile('MonteCarlo_Result_hogehoge.txt'): 
              os.remove('MonteCarlo_Result_hogehoge.txt')

            # use while loop as the simulation often fails
            while( not os.path.isfile('MonteCarlo_Result_hogehoge.txt') ):
                # mocadi_func('_sweep',X)
                mocadi.RunMocadi(X)
                ratio = mocadi.LoadMocadiResults()
            print("Output : " + str(ratio) )
            Y[idx][idx_1d] = ratio
  
    figure(figsize = (8, 6))
    plt.title("Plotting a2-D array")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    
    for i, array in enumerate(Y):
        plt.plot(X_1d, array, marker = "o", label = f"Array #{i}")
  
    plt.legend(loc = "center left", bbox_to_anchor=(1, 0.5))
    plt.savefig("plot_out_2d.png")
    plt.show()

    np.save('array_Y.npy',Y)


