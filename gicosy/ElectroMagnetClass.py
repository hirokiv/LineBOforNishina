import os.path
import time
import numpy as np
import sys
import shutil
from febo.utils import get_logger

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from febo.utils.config import ConfigField, Config, Configurable, assign_config


logger = get_logger("emconfig")

# initial BQ values (hard-coded)

class EMConfig(Config):
    multiple_factor = ConfigField(1.5)
    _section = 'emsetup'


@assign_config(EMConfig)
class ElectroMagnetClass(Configurable):
    def __init__(self):
        self.BQ0 = np.atleast_2d([
            0.000,
            -0.313,
            0.206,
            0.195,
            -0.207,
            0.000,
            0.195,
            0.198,
            -0.190,
            -0.287,
            0.332,
            -0.695,
            0.622,
            -0.026,
            0.537,
            -0.626,
            0.906
            # -3.58757E-01,
            # -8.50502E-03,
            # 0.180925008,
            # 0.265975226,
            # -0.0,
            # -0.00136544,
            # 0.044999297,
            # 0.364942752,
            # -0.42834382,
            # -0.4391684,
            # 0.34020087,
            # -0.29690258,
            # 0.53968229,
            # -0.25515065,
            # 0.740710077,
            # -0.6154543,
            # 0.511847673    
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
        logger.info('###############################')
        logger.info('show X0')
        logger.info('###############################')
        logger.info(self.X0)
        # print(self.BQ0)
        # print(self.BQave)
        # print(self.BQ_factor)

    def getX0(self):
        return self.X0

    def setBQRange(self):
        # temporaly based on polarity and 1 maximum
        BQ0_multiplied = np.abs(self.BQ0 * self.config.multiple_factor) # allow 4 times multiple for each
        self.BQmax = BQ0_multiplied * (np.atleast_2d([0 if i<0 else i for i in self.polarity.flatten()]))
        self.BQmin = BQ0_multiplied * (np.atleast_2d([0 if i>0 else i for i in self.polarity.flatten()]))
        self.BQave = (self.BQmax + self.BQmin) / 2.
        self.BQ_factor = self.BQmax - self.BQave
        logger.info('###############################')
        logger.info('setBQRange called')
        logger.info('show max, min, ave, BQ_factor')
        logger.info('###############################')
        logger.info(self.BQmax)
        logger.info(self.BQmin)
        logger.info(self.BQave)
        logger.info(self.BQ_factor)

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
        # logger.info('#########################################################')
        # logger.info('## Evaluate_Envelope_mocadi.py getBQ ##')
        # logger.info('#########################################################')
        # logger.info(self.BQ.flatten())
        return self.BQ.flatten()

    def getBQ0(self):
        return self.BQ0.flatten()

    def getPolarity(self):
        return self.polarity.flatten()

 
