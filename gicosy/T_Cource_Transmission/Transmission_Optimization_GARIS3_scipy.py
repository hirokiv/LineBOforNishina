import sys
import os
import re
import Func_Edit_Files
import Ana_Root_Transmission
import time
import math

from scipy.optimize import minimize

#method_opt="Nelder-Mead"
#options_input={"disp":1,"maxfev":1000}
method_opt="Powell"
options_input={"disp":1}
#method_opt="L-BFGS-B"
#method_opt="TNC"
#method_opt=""
#options_input={"disp":1,"maxiter":100,"maxfun":100}
#options_input={"disp":1}
ActiveQ_Num = 7
factor_transmission = 1;
ndata=10000
nelement_init = 13
Init_Gicosy=0
Init_Mocadi=0
Flag_Fit   =0

# sigXmm  =0.87
# sigAmrad=1.76
# CorrerationH = 0.058
# sigYmm  =1.06
# sigBmrad=1.21
# CorrerationV = 0.003
# sigP=0.5

factor_spot    = 10.
#spot_shape_h_v = 2.0
x_spot_goal = 3.0
y_spot_goal = 0.5
duct_scale_factor=0.5
dist_shape = 2 # 0:fixed 1: flat 2: gaus 

beam_Q=13
beam_A=51
beam_Au=50.936825
#beam_MeVu=6.00799
#beam_MeVu=6.0077
beam_MeVu=6.013
#beam_MeVu=3.6
flag_calc_1st_order=0

#2021Dec6th
sigXmm  =	0.61
sigAmrad=	2.03
CorrerationH = 	0.13
sigYmm  =	0.90
sigBmrad=	1.40
CorrerationV =  -0.02
#sigP=0.06
sigP=0.04


BQ = [
    # -0.27732,
    # +0.23784, 
    # -0.28195, 
    # +0.19915, 
    # -0.17028,
    # +0.23995,
    # -0.22705
    #2020July21st
    # -0.38836,
    # 0.26287,
    # -0.30637,
    # 0.16658,
    # -0.16686,
    # 0.26392,
    # -0.27487
    #2020Oct17th
    # -0.24781,
    # 0.24467,
    # -0.26551,
    # 0.19915,
    # -0.17459,
    # 0.24677,
    # -0.25170
    #2020Nov30th
    # -0.28637,
    # 0.24868,
    # -0.30055,
    # 0.19730,
    # -0.16864,
    # 0.26004,
    # -0.25793
    #2020Dec10th
    # -0.36604,
    # 0.26517,
    # -0.30283,
    # 0.19915,
    # -0.17212,
    # 0.24297,
    # -0.22194
    #2020Dec14th
    # -0.27732,
    # 0.23971,
    # -0.28107,
    # 0.19121,
    # -0.14920,
    # 0.25290,
    # -0.26843
    #2021May21st
    # -0.27732,
    # 0.23971,
    # -0.28227,
    # 0.18441,
    # -0.17323,
    # 0.23891,
    # -0.26376
    #2021May28th
    # -0.27089,
    # 0.23024,
    # -0.29421,
    # 0.17639,
    # -0.17033,
    # 0.24378,
    # -0.25271
    #2021June3rd
    # -0.26765,
    # 0.21187,
    # -0.26966,
    # 0.16896,
    # -0.15919,
    # 0.25271,
    # -0.24378
    #2021June10th
    # -0.26765,
    # 0.21842,
    # -0.26804,
    # 0.16896,
    # -0.15919,
    # 0.25271,
    # -0.24540

    #2021June3rd_mocadi_1st_try
    # -0.00000,
    # +0.231305,
    # -0.268323,
    # +0.103080,
    # -0.166376,
    # +0.233436,
    # -0.229772

    #2021May21st_mocadi_1st_try
    # -0.172219,
    # +0.241905,
    # -0.282590,
    # +0.184406,
    # -0.173237,
    # +0.263763,
    # -0.238896

    #2021June7th
    # -0.26765,
    # 0.20695,
    # -0.26966,
    # 0.16896,
    # -0.15919,
    # 0.25271,
    # -0.24378

    #2021June18th
    # -0.26765,
    # 0.23511,
    # -0.26804,
    # 0.16896,
    # -0.15919,
    # 0.22835,
    # -0.23569

    #2021June30th
    # -0.29027,
    # 0.26468,
    # -0.29388,
    # 0.16896,
    # -0.15919,
    # 0.24784,
    # -0.25676

    #2021June30th_2nd
    # -0.32720,
    # 0.26468,
    # -0.30676,
    # 0.17639,
    # -0.15641,
    # 0.25595,
    # -0.25676

    #2021July Dispersion
    #  -1.780001971E-02,
    #  1.578017221E-01,
    # -1.843208829E-01,
    # 1.460302884E-01,
    # -1.235062296E-01,
    # 1.968291908E-01,
    # -1.915995141E-01    
    
    # fit result in 2021May21st
    # -0.172219,#BQTa
    # 0.241905,#BQTb
    # -0.282590,#BQTc
    # 0.184406,#BQS1
    # -0.173237,#BQS2
    # 0.263763,#BQDa
    # -0.238896 #BQDb

    #FitResult_2021July7th_high_transmission_wMeasuredEmittance.txt
    # -0.388311,
    # +0.250240,
    # -0.244239,
    # +0.198923,
    # -0.165332,
    # +0.262787,
    # -0.267796

    # -0.316612,#BQTa
    # +0.250240,#BQTb
    # -0.244239,#BQTc
    # +0.205377,#BQS1
    # -0.171671,#BQS2
    # +0.262787,#BQDa
    # -0.267796 #BQDb

    #July8th_final
    # -0.21010,
    # 0.25053,
    # -0.23260,
    # 0.19971,
    # -0.18135,
    # 0.26619,
    # -0.27888

    #July7th Hellipse 
    # -0.354851, 
    # 0.250809, 
    # -0.243804, 
    # 0.192917, 
    # -0.165668, 
    # 0.280455, 
    # -0.269364
    #2021 Oct24th transmission
    # -0.354851,#BQTa
    # 0.250809,#BQTb
    # -0.296273,#BQTc
    # 0.189289,#BQS1
    # -0.165668,#BQS2
    # 0.277238,#BQDa
    # -0.307085 #BQDb

    #2021 Oct26th Hellipse (not used)
    # -0.461295,#BQTa
    # +0.282182,#BQTb
    # -0.299338,#BQTc
    # +0.189914,#BQS1
    # -0.144897,#BQS2
    # +0.277815,#BQDa
    # -0.307488 #BQDb

    #2021 Nov9th test
    # -0.,#BQTa
    # +0.282182,#BQTb
    # -0.299338,#BQTc
    # +0.189914,#BQS1
    # -0.144897,#BQS2
    # +0.277815,#BQDa
    # -0.307488 #BQDb

    #2021 Nov25th HighTransmission
    # -0.336460,#BQTa
    # +0.250891,#BQTb
    # -0.257897,#BQTc
    # +0.217126,#BQS1
    # -0.183889,#BQS2
    # +0.265605,#BQDa
    # -0.272689 #BQDb

    #2021 Nov25th Hellipse
    # -0.287077,#BQTa
    # +0.241187,#BQTb
    # -0.256477,#BQTc
    # +0.220941,#BQS1
    # -0.179191,#BQS2
    # +0.245367,#BQDa
    # -0.275725 #BQDb

    # -0.287077,
    # 0.241187,
    # -0.275177,
    # 0.211414,
    # -0.180735,
    # 0.290821,
    # -0.278591

    #2021 Nov25th Hellipse v2
    # -0.287077,
    # 0.241187,
    # -0.256477,
    # 0.220941,
    # -0.179191,
    # 0.290821,
    # -0.278591
    #2021 Dec. 6th gicosy calc default
    # -0.28779,
    # 0.24753,
    # -0.26078,
    # 0.22094,
    # -0.17919,
    # 0.23615,
    # -0.23673
    #2021 Dec. 6th gicosy calc OpeMod
    # -0.28779,
    # 0.24753,
    # -0.26078,
    # 0.21983,
    # -0.17455,
    # 0.21989,
    # -0.24323
    #2021 Dec. 6th python calc QDb mod
    -0.36524,
    0.24142,
    -0.26055,
    0.15488,
    -0.17919,
    # -0.17455,
    0.28760,
    -0.27858
    #2021 Dec. 6th python calc QSe12 QDb mod
    # -0.36524,
    # 0.24142,
    # -0.26055,
    # 0.15488,
    # -0.17455,
    # 0.28760,
    # -0.27858            
    #2021 Nov25th Small Spot from FitData
#     -0.392963,
#     0.256994,
#     -0.253581,
# #    0.306725,
#     0.20725,
#     -0.182437,
#     0.286480,
#     -0.273941    
    #July8th_Hellipse_2
    # -0.210098,#BQTa
    # +0.250521,#BQTb
    # -0.256946,#BQTc
    # +0.199710,#BQS1
    # -0.181336,#BQS2
    # +0.296890,#BQDa
    # -0.278888 #BQDb

    #July8th_e12_dispersion_positive
    # -0.38813, 
    # +0.25010, 
    # -0.24410, 
    # +0.28135, 
    # -0.17228, 
    # +0.26266, 
    # -0.26765 
    
    #2021July Hellipse_gicosy
    # -0.388118, 
    # 0.252030, 
    # -0.256795, 
    # 0.185270, 
    # -0.126793, 
    # 0.241685, 
    # -0.280402
    #2021July Hellipse_python
    # -0.341933,#BQTa
    # +0.245104,#BQTb
    # -0.244056,#BQTc
    # +0.198219,#BQS1
    # -0.156416,#BQS2
    # +0.275255,#BQDa
    # -0.267551 #BQDb    
]
Bmax=0.400
bounds_BQ=(
#    (-0.480,+0.001),#BQTa
    (-Bmax ,+0.001),#BQTa
    ( 0.001,+Bmax),#BQTb    
    (-Bmax ,+0.001),#BQTc
#    ( 0.001,+Bmax),#BQS1
    ( 0.001,+0.25),#BQS1
    (-0.25 ,+0.001),#BQS2
    ( 0.001,+Bmax),#BQDa
    (-Bmax ,+0.001) #BQSb
    )
#Dipole_num=[5,8,11,14,15]

data_lines=None

os.system('cp ./gicosy_dat/HEBT_GARIS3_fit_org.dat ./')


def eval_f_GARIS3(x,args):
    start = time.time()
    flag_track = 0
    print(x)
    Func_Edit_Files.Edit_gicosy_GARIS3(Beam,args[0],x,"HEBT_GARIS3_fit_org.dat",flag_track)
    os.system('./gicosy_forLoop.sh HEBT_GARIS3%s.dat > gicosy_output.txt'%(args[0]))
    with open("gicosy_output.txt",encoding = "utf-8",mode="r") as f_gicosy_result:
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

    eval_func = 0.0
    x_spot = 0
    y_spot = 0
    if factor_spot > 0.:
        print("factor spot is active!")
        x_spot = math.sqrt((xx_val * Beam.sigmaXfp_mm)**2 + (xa_val * Beam.sigmaA_mrad)**2 + (xd_val * Beam.sigmaP)**2)
        y_spot = math.sqrt((yy_val * Beam.sigmaYfp_mm)**2 + (yb_val * Beam.sigmaB_mrad)**2)
        #eval_func = eval_func + (x_spot / y_spot - spot_shape_h_v)**2 * factor_spot
        eval_func = eval_func + ( (x_spot - x_spot_goal)**2 + (y_spot - y_spot_goal)**2 ) * factor_spot
        print("x spot %lf y spot %lf contribution for eval_func %lf \n"%(x_spot,y_spot,eval_func))
    if factor_transmission > 0:
        print("factor transmission is active!")
        os.system('mocadiR40 HEBT_GARIS3%s.in'%(args[0]))
        loss = Ana_Root_Transmission.Ana_transmission_GARIS3(filename_root,nelement)
        eval_func = eval_func + loss * factor_transmission
    
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print("x_spot %lf y_spot %lf  goal %lf/%lf"%(x_spot,y_spot,x_spot_goal,y_spot_goal))
    print("eval_func = %lf"%eval_func)
    for param in x:
#        print("%lf"%x[iparam],end='')
        f_fit_data.write("%lf "%param)
#        print(param,end=' ')
    f_fit_data.write("%lf "%x_spot)
    f_fit_data.write("%lf "%y_spot)
    f_fit_data.write("%lf "%loss)
    f_fit_data.write("%lf\n"%eval_func)
    print("")
    return eval_func

args_sys = sys.argv
print("# of args = ",len(args_sys))
if len(args_sys) <= 2:
    print ("Usage: python Transmission_Optimizationn_GARIS3_scipy.py filename_output Init_Gicosy Init_MOCADI Flag_Fit")
    exit()
if len(args_sys) > 2:
    Init_Gicosy = int(args_sys[2])
if len(args_sys) > 3:    
    Init_Mocadi = int(args_sys[3])
if len(args_sys) > 4:    
    Flag_Fit    = int(args_sys[4])
    
#filename_root="./Root/HEBT_Alpha%s_geo_%s_%dsample_%delement.root"%(args_sys[1],geo,ndata,nelement_init)
filename_root="./HEBT_GARIS%s.root"%(args_sys[1])

Beam = Func_Edit_Files.Beam_proparty(    
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

if Init_Gicosy == 1:
    flag_track = 1
    Func_Edit_Files.Edit_gicosy_GARIS3(Beam,args_sys[1],BQ,"HEBT_GARIS3_fit_org.dat",flag_track)
    os.system('./gicosy.sh HEBT_GARIS3%s.dat > gicosy_output.txt'%(args_sys[1]))


    with open("gicosy_output.txt",encoding = "utf-8",mode="r") as f_gicosy_result:
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
        
Func_Edit_Files.Edit_MatrixInit_GARIS3(Beam)

if Init_Mocadi == 1:
    filename_root, nelement = Func_Edit_Files.Edit_mocadi_GARIS3(args_sys[1],Beam,ndata,flag_calc_1st_order,dist_shape,duct_scale_factor)
    os.system('mocadiR40 HEBT_GARIS3%s.in'%(args_sys[1]))

    print(filename_root)
    print("element number is ", nelement)
    
if Flag_Fit == 1:
    f_fit_data=open('FitData%s.txt'%(args_sys[1]),'w')
#    result = minimize(fun = eval_f_GARIS3,x0 = BQ,args = [args_sys[1]],method=method_opt,options=options_input)
    result = minimize(fun = eval_f_GARIS3,x0 = BQ,args = [args_sys[1]],method=method_opt,options=options_input,bounds = bounds_BQ)
    print(result)
    f_fit_data.close()
    print("""
BQ = [
%lf,#BQTa
%lf,#BQTb
%lf,#BQTc
%lf,#BQS1
%lf,#BQS2
%lf,#BQDa
%lf #BQDb
]"""%(result.x[0],result.x[1],result.x[2],result.x[3],result.x[4],result.x[5],result.x[6]))

    f_result=open('FitResult%s.txt'%(args_sys[1]),'w')
    f_result.write(result.message)
    f_result.write("""
    fun: %lf
message: %s
   nfev: %d
    nit: %d
 status: %d
success: %s
"""%(result.fun,result.message,result.nfev,result.nit,result.status,result.success)
)
    f_result.write("""
BQ = [
%+lf,#BQTa
%+lf,#BQTb
%+lf,#BQTc
%+lf,#BQS1
%+lf,#BQS2
%+lf,#BQDa
%+lf #BQDb
]"""%(result.x[0],result.x[1],result.x[2],result.x[3],result.x[4],result.x[5],result.x[6]))    
    f_result.close()

    f_result_QB=open('QB_FitResult%s.txt'%(args_sys[1]),'w')
    f_result_QB.write("""%+lf
%+lf
%+lf
%+lf
%+lf
%+lf
%+lf
"""%(result.x[0],result.x[1],result.x[2],result.x[3],result.x[4],result.x[5],result.x[6]))    
    f_result_QB.close()
    
    os.system('mv ./FitResult%s.txt ./Txt_FitResult/'%(args_sys[1]))
    os.system('mv ./QB_FitResult%s.txt ./Txt_FitResult/'%(args_sys[1]))
if Flag_Fit == 1:
    BQ_result = result.x
else:
    BQ_result = BQ
flag_track = 1

Func_Edit_Files.Edit_gicosy_GARIS3(Beam,args_sys[1],BQ_result,"HEBT_GARIS3_fit_org.dat",flag_track)
os.system('./gicosy.sh HEBT_GARIS3%s.dat > gicosy_output.txt'%(args_sys[1]))
if Init_Mocadi + Flag_Fit > 0:
    Ana_Root_Transmission.Ana_transmission_GARIS3(filename_root,nelement)
print("x_spot %lf y_spot %lf  goal %lf/%lf"%(x_spot,y_spot,x_spot_goal,y_spot_goal))


os.system('mv ./HEBT_GARIS3%s.root ./Root/HEBT_GARIS3%s_%dsample_%delement.root'%(args_sys[1],args_sys[1],ndata,nelement))
os.system('mv ./*.pdf ./pdf/')
os.system('mv ./*.ps ./pdf/')
os.system('mv ./*.dat ./gicosy_dat/')
os.system('mv ./*.in ./mocadi_in/')
os.system('mv ./*.out ./mocadi_in/')

