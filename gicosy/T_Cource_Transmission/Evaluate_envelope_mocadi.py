import sys
import os
import re
from .Func_Edit_Files import Beam_proparty, Edit_gicosy_TCource, Edit_MatrixInit_EBM, Edit_mocadi_TCource
from febo.utils import get_logger
# import Ana_Root_Transmission
import time
import math
import numpy as np

def mocadi_func(*args):
    # args[0] : identifier
    # args[1] : path

    # virtually generate args_sys
    arg1 = 'virtual_arg1'
    args_sys = [arg1, args[0], args[1], args[2]]

    print('Evaluate_envelope_mocadi.py : args_sys')
    print(args_sys)

    X_BQ = args_sys[2] # this should contain normalized scale between (-1,1)
    BQConfig = args_sys[3]
    BQConfig.setBQ(X_BQ)

    # Bmax=0.400
    # . bounds_BQ=(
    # #    (-0.480,+0.001),#BQTa
    #     (-Bmax ,+0.001),#BQTa
    #     ( 0.001,+Bmax),#BQTb    
    #     (-Bmax ,+0.001),#BQTc
    # #    ( 0.001,+Bmax),#BQS1
    #     ( 0.001,+0.25),#BQS1
    #     (-0.25 ,+0.001),#BQS2
    #     ( 0.001,+Bmax),#BQDa
    #     (-Bmax ,+0.001) #BQSb
    #     )
    # #Dipole_num=[5,8,11,14,15]
    
    
    ndata=10000
    nelement_init = 12
    
    duct_scale_factor=0.5
    dist_shape = 2 # 0:fixed 1: flat 2: gaus 
    
    beam_Q=86
    beam_A=238
    beam_Au=238.004
    beam_MeVu=345
    
    flag_calc_1st_order=0
    
    # monochromatic beam parameter at EBM (1 sigma)
    
    emittance_h = 0.25
    beta_h      = 1.0
    alpha_h     = 0.5
    gamma_h     = (1 + alpha_h * alpha_h)/beta_h
    
    emittance_v = 0.5
    beta_v      = 2.0
    alpha_v     = -0.5
    gamma_v     = (1 + alpha_v * alpha_v)/beta_v
    
    sigP=0.1 # parcent
    
    sigXmm  =       math.sqrt(beta_h  * emittance_h)
    sigAmrad=	math.sqrt(gamma_h * emittance_h)
    CorrerationH =  alpha_h * emittance_h / (sigXmm * sigAmrad)
    sigYmm  =	math.sqrt(beta_v  * emittance_v)
    sigBmrad=	math.sqrt(gamma_v * emittance_v)
    CorrerationV =  alpha_v * emittance_h / (sigYmm * sigBmrad)
    #sigP=0.06
    
    flag_track = 1
    
   
    data_lines=None
    
    os.system('cp ./gicosy_dat/EBM-BigRIPS_org.dat ./')
    
    
    
    print("# of args = ",len(args_sys))
    if len(args_sys) <=  2:
        print ("Usage: python Evaluate_envelope_mocadi.py filename_output ")
        exit()
    
    
    Beam = Beam_proparty(    
        sigmaX_mm   = sigXmm,
        sigmaA_mrad = sigAmrad,
        CorrH       = CorrerationH,
        sigmaY_mm   = sigYmm,
        sigmaB_mrad = sigBmrad,    
        CorrV       = CorrerationV,
        sigmaP      = sigP,
        beam_Q      = beam_Q,
        beam_Au     = beam_Au,
        beam_MeVu   = beam_MeVu
    )
    
    nelement = nelement_init
    x_spot = 0
    y_spot = 0

    BQ_file = np.round(BQConfig.getBQ(), 6).tolist()
    #Edit_gicosy_TCource(Beam,args_sys[1],BQ,"./EBM-BigRIPS_org.dat",flag_track)
    Edit_gicosy_TCource(Beam,args_sys[1],BQ_file,"./EBM-BigRIPS_org.dat",flag_track)
    os.system('./gicosy.sh ./EBM-BigRIPS%s.dat > ./gicosy_output.txt'%(args_sys[1]))
    
    
    with open("./gicosy_output.txt",encoding = "utf-8",mode="r") as f_gicosy_result:
        data_lines = f_gicosy_result.read()
        xx = re.findall('ME11  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)                
        xa = re.findall('ME12  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)
        ax = re.findall('ME21  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)
        xd = re.findall('ME16  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)
        yy = re.findall('ME33  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)                
        yb = re.findall('ME34  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)
        by = re.findall('ME43  = ([ \-]?[0-9].[0-9]{9}E[+\-]?[0-9]{2});',data_lines)
        print("xx =",xx[0])
        print("xa =",xa[0])
        print("ax =",ax[0])
        print("xd =",xd[0])
        print("yy =",yy[0])
        print("yb =",yb[0])
        print("by =",by[0])
        xx_val = float(xx[0])
        xa_val = float(xa[0])
        ax_val = float(ax[0])
        xd_val = float(xd[0]) * 10 # mm/%
        yy_val = float(yy[0])
        yb_val = float(yb[0])
        by_val = float(by[0])
        x_spot = math.sqrt((xx_val * Beam.sigmaXfp_mm)**2 + (xa_val * Beam.sigmaA_mrad)**2 + (xd_val * Beam.sigmaP)**2)
        y_spot = math.sqrt((yy_val * Beam.sigmaYfp_mm)**2 + (yb_val * Beam.sigmaB_mrad)**2)
        
    Edit_MatrixInit_EBM(Beam)
    
    filename_hbk, nelement = Edit_mocadi_TCource(args_sys[1],Beam,ndata,flag_calc_1st_order,dist_shape,duct_scale_factor)
    os.system('mocadi-42e ./EBM-BigRIPS%s.in > ./log/mocadi-42e_output.txt'%(args_sys[1]))
    os.system('h2root ./ebm-bigrips%s.hbk    > ./log/h2root_output.txt'%(str.lower(args_sys[1])))
    os.system('mv ./ebm-bigrips%s.root ./EBM-BigRIPS%s.root'%(str.lower(args_sys[1]),args_sys[1]))
    #     print(filename_root)
    print("element number is ", nelement)
        
    os.system('root \"./Ana_MOCADI_v2.C(\\\"./EBM-BigRIPS%s.root\\\",%d,\\\"%s\\\")\" -q -b > ./log/root_Ana_MOCADI_output.txt'%(args_sys[1],nelement,args_sys[1]))
    
    os.system('mv ./EBM-BigRIPS%s.root ./Root/EBM-BigRIPS%s_%dsample_%delement.root'%(args_sys[1],args_sys[1],ndata,nelement))
    os.system('mv ./*.eps ./figure/')
    os.system('mv ./*.ps ./figure/')
    os.system('mv ./*.dat ./gicosy_dat/')
    os.system('mv ./*.in ./mocadi_in/')
    os.system('mv ./*.out ./mocadi_in/')
    
if __name__ == '__main__':

    args_sys = sys.argv
    #X0 = np.atleast_2d(np.zeros(17))

    X_1d = np.linspace(-1, 1, 10)

    # loop until error occurs
    if os.path.isfile('MonteCarlo_Result_hogehoge.txt'):
        os.remove('MonteCarlo_Result_hogehoge.txt')

    BQConfig = ElectroMagnetConfig()
    X0 = BQConfig.getX0()
    print(X0)
    while( not os.path.isfile('MonteCarlo_Result_hogehoge.txt') ):
        mocadi_func('_hogehoge',X0, BQConfig)
        os.remove('MonteCarlo_Result_hogehoge.txt')

    print('Error occured')
