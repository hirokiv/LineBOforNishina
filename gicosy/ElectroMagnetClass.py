import os.path
import time
import numpy as np
import sys
import shutil
from enum import Enum
from febo.utils import get_logger

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from febo.utils.config import ClassListConfigField, ConfigField, Config, Configurable, assign_config, EnumConfigField


logger = get_logger("emconfig")

class BQSetMode(Enum):
    multiplication = 1
    hardcode = 2
    scalar = 3

# contains default value which is manageable by gicosy_interface.yaml
class EMConfig(Config):
    # initial BQ values (hard-coded)
    polarity = [
           -1,-1,+1,+1,
            -1,-1,+1,
            +1,-1,
            -1,+1,
            -1,+1,-1,
            +1,-1,+1
        ]
    BQ0temp =[
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
            0.906] 
    BQ0 = ConfigField(BQ0temp, field_type = list, allow_none = False)
    # field for multiplication mode
    multiple_factor = ConfigField(1.5)
    # fields for hard code mode
    em_scalar = ConfigField(0.2)
    BQ_max = ConfigField( np.array(BQ0temp) , field_type = list, allow_none = False)
    BQ_min = ConfigField( np.array(BQ0temp) , field_type = list, allow_none = False)
    # switch BQ max and min set mode
    BQSETMODE = EnumConfigField('multiplication', enum_cls=BQSetMode, comment='Can be set to "multiplication", "hardcode", or "scalar".')
    _section = 'emsetup'


@assign_config(EMConfig)
class ElectroMagnetClass(Configurable):
    def __init__(self):
        self.BQ0 = np.atleast_2d( self.config.BQ0 ) # initialize as 2d array
    
        # note for later restricting the input value
        self.polarity = np.atleast_2d(self.config.polarity)

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
        logger.info('##  show X0                  ##')
        logger.info(self.X0)

    def getX0(self):
        return self.X0

    def setBQRange(self):
        if self.config.BQSETMODE.name == 'multiplication':
            # Set BQ based on polarity and multiplied maximum
            BQ0_multiplied = np.abs(self.BQ0 * self.config.multiple_factor) # allow 4 times multiple for each
            self.BQmax = BQ0_multiplied * (np.atleast_2d([0 if i<0 else i for i in self.polarity.flatten()]))
            self.BQmin = BQ0_multiplied * (np.atleast_2d([0 if i>0 else i for i in self.polarity.flatten()]))
        elif self.config.BQSETMODE.name == 'hardcode':
            # Hard code max and min value
            self.BQmax = np.atleast_2d(self.config.BQ_max)
            self.BQmin = np.atleast_2d(self.config.BQ_min)
        elif self.config.BQSETMODE.name == 'scalar':
            # add or subtract scalar value from the entire matrix
            self.BQmax = np.array(self.config.BQ0) + self.config.em_scalar
            self.BQmin = np.array(self.config.BQ0) - self.config.em_scalar


        self.BQave = (self.BQmax + self.BQmin) / 2.
        self.BQ_factor = self.BQmax - self.BQave
        logger.info('###################################')
        logger.info('## setBQRange called             ##')
        logger.info('## show max, min, ##')
        logger.info(self.BQmax)
        logger.info(self.BQmin)
        #logger.info(self.BQave)
        #logger.info(self.BQ_factor)

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

 
