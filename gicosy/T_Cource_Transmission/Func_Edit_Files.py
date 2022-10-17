import os
import sys
import re
import math

Dipole_num=[5,8,11,14]
Dipole_num_GARIS3=[6]

duct_D45 = 2.0
unit_mass = 931.49400
class Beam_proparty:
    def __init__(self,sigmaX_mm=1.0,sigmaA_mrad=1.0,CorrH=0,sigmaY_mm=1.0,sigmaB_mrad=1.0,CorrV=0,sigmaP=0.1,beam_Q=2,beam_Au=4,beam_MeVu=7.25):
        self.sigmaX_mm  =sigmaX_mm
        self.sigmaA_mrad=sigmaA_mrad
        self.CorrH      =CorrH
        self.sigmaXA    = CorrH * sigmaX_mm * sigmaA_mrad
        self.EpsilonX   = sigmaX_mm * sigmaA_mrad * math.sqrt(1 - CorrH * CorrH)
        self.sigmaXfp_mm= sigmaX_mm * math.sqrt(1 - CorrH * CorrH)
        self.sigmaY_mm  =sigmaY_mm
        self.sigmaB_mrad=sigmaB_mrad
        self.CorrV      =CorrV
        self.sigmaYB = CorrV * sigmaY_mm * sigmaB_mrad
        self.EpsilonV   = sigmaY_mm * sigmaB_mrad * math.sqrt(1 - CorrV * CorrV)
        self.sigmaYfp_mm= sigmaY_mm * math.sqrt(1 - CorrV * CorrV)
        self.sigmaP     =sigmaP
        self.beam_Q    = beam_Q
        self.beam_Au   = beam_Au
        self.beam_A    = int(beam_Au)
        self.beam_MeVu = beam_MeVu
        self.beam_T    = beam_MeVu * beam_Au 
        self.beam_beta = sigmaP/(self.beam_T + self.beam_Au * unit_mass)
        self.beam_gamma= 1./math.sqrt(1. - self.beam_beta * self.beam_beta)

def Edit_gicosy_TCource(Beam,extra_name,BQ,filename_base = "EBM-BigRIPS_org.dat",flag_track = 0):
    os.system('cp %s EBM-BigRIPS%s.dat'%(filename_base,extra_name))

    file_name_gicosy     = "EBM-BigRIPS%s.dat"%(extra_name)
    with open(file_name_gicosy,encoding = "utf-8",mode="r") as f_gicosy:
        data_lines = f_gicosy.read()        

        if flag_track == 1:
            
#            data_lines = data_lines.replace(";D B   .1   .1   1000  3 3 1 3 3 3 3;","D B   .1   .1   1000  3 3 1 3 3 3 3;")
            data_lines = re.sub(r"; D B  (.*)",r"D B  \1",data_lines)
            data_lines = re.sub(r"; D H E (.*)",r"D H E \1",data_lines)
            data_lines = re.sub(r"; D E (.*)"  ,r"D E \1"  ,data_lines)
            data_lines = data_lines.replace(";D S   .2   2   100    3 3 1 1 1 1;","D S   .2   2   100    3 3 1 1 1 1;")
            data_lines = data_lines.replace(";D F   .2 1.0 2.2;",";D F   .2 1.0 2.2;")
            data_lines = data_lines.replace("; D E 0.2 10 100 ([X,D]) ; dispersion","D E 0.2 10 100 ([X,D]) ; dispersion")
#            data_lines = data_lines.replace("; Goto Subroutine InitialPhase;","Goto Subroutine InitialPhase;")            
#            data_lines = data_lines.replace(";Goto Subroutine SRCMAT;","Goto Subroutine SRCMAT;")

        data_lines = data_lines.replace(
            """
ENERGY = 320; 
MASS   = 238;
CHARGE = 86;
""",
            """
ENERGY = %lf; 
MASS   = %lf;
CHARGE = %lf;
"""%(Beam.beam_MeVu * Beam.beam_Au,
                 Beam.beam_Au,
                 Beam.beam_Q
            )                
        )
            
        data_lines = data_lines.replace(
            """xx    =  1.^2 * 4.0e-6;
aa    =  1.^2 * 4.0e-6;
CorrH = 0;
yy    =  1.^2 * 4.0e-6;
bb    =  1.^2 * 4.0e-6;
CorrV = 0;
""",
            """xx    =  %lfe-6;
aa    =  %lfe-6;
CorrH = %lf;
yy    =  %lfe-6;
bb    =  %lfe-6;
CorrV = %lf;
"""%(Beam.sigmaX_mm   * Beam.sigmaX_mm  ,
     Beam.sigmaA_mrad * Beam.sigmaA_mrad,
     Beam.CorrH,
     Beam.sigmaY_mm   * Beam.sigmaY_mm  ,
     Beam.sigmaB_mrad * Beam.sigmaB_mrad,
     Beam.CorrV
     )
    )
        data_lines = data_lines.replace("IP         = 0.001; +-Momentum Acceptance","IP         = %lf;"%(Beam.sigmaP/100.) )
            


        data_lines = data_lines.replace(
"""; Bvalues
  BQUT1 = 1.0 ; 
  BQMT1 = 1.0 ; 
  BQDT1 = 1.0 ; 
  BQET1 = 1.0 ; 
  BQUT2 = 1.0 ; 
  BQMT2 = 1.0 ; 
  BQDT2 = 1.0 ; 
  BQUT3 = 1.0 ; 
  BQDT3 = 1.0 ; 
;
  BQUT4 = 1.0 ;
  BQDT4 = 1.0 ;
  BQUT5 = 1.0 ;
  BQMT5 = 1.0 ;
  BQDT5 = 1.0 ;
  BQUT6 = 1.0 ;
  BQMT6 = 1.0 ;
  BQDT6 = 1.0 ;""",
"""; Bvalues
  BQUT1 = %lf ; 
  BQMT1 = %lf ; 
  BQDT1 = %lf ; 
  BQET1 = %lf ; 
  BQUT2 = %lf ; 
  BQMT2 = %lf ; 
  BQDT2 = %lf ; 
  BQUT3 = %lf ; 
  BQDT3 = %lf ; 
;
  BQUT4 = %lf ;
  BQDT4 = %lf ;
  BQUT5 = %lf ;
  BQMT5 = %lf ;
  BQDT5 = %lf ;
  BQUT6 = %lf ;
  BQMT6 = %lf ;
  BQDT6 = %lf ;
;"""%(
    BQ[ 0],BQ[ 1],BQ[ 2],BQ[ 3],
    BQ[ 4],BQ[ 5],BQ[ 6],
    BQ[ 7],BQ[ 8],
    BQ[ 9],BQ[10],
    BQ[11],BQ[12],BQ[13],
    BQ[14],BQ[15],BQ[16]
)

        )
    with open(file_name_gicosy,encoding = "utf-8",mode="w") as f_gicosy:            
        f_gicosy.write(data_lines)

        
def Edit_MatrixInit_EBM(Beam):
    file_name_matrix         = "./matrix/SRCBIGRIPS000_unit.MAT"
    file_name_matrix_out     = "./matrix/SRCBIGRIPS000.MAT"
    data_lines=None
    sigma_x = Beam.sigmaX_mm
    sigma_a = Beam.sigmaA_mrad
    sigma_y = Beam.sigmaY_mm
    sigma_b = Beam.sigmaB_mrad

    xa = Beam.CorrH * Beam.sigmaX_mm * Beam.sigmaA_mrad
    yb = Beam.CorrV * Beam.sigmaY_mm * Beam.sigmaB_mrad

    with open(file_name_matrix,encoding = "utf-8") as f_in:
        data_lines = f_in.read()        
        data_lines = data_lines.replace("   2 A      0.000000E+00  1.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00",
                                        "   2 A     %+6e  1.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00"%(Beam.CorrH * Beam.sigmaX_mm/Beam.sigmaA_mrad))
        data_lines = data_lines.replace("   4 B      0.000000E+00  0.000000E+00  0.000000E+00  1.000000E+00  0.000000E+00",
                                        "   4 B      0.000000E+00  0.000000E+00 %+6e  1.000000E+00  0.000000E+00"%(Beam.CorrV * Beam.sigmaY_mm/Beam.sigmaB_mrad))

    with open(file_name_matrix_out,mode="w",encoding = "utf-8") as f_out:
        f_out.write(data_lines)

        
def Edit_mocadi_TCource(extra_name,Beam,ndata,flag_calc_1st_order,dist_shape = 2, duct_scale_factor = 1.0):
    os.system('./gicosy2mocadif EBM-BIGRIPS%s_out.dat'%extra_name)
    file_name_mocadi     = "GICOSYOUT.in"
    file_name_mocadi_out = "EBM-BigRIPS%s.in"%extra_name
    data_lines=None
        
    with open(file_name_mocadi,encoding = "utf-8") as f_in:
        data_lines = f_in.read()        

        # beam        
        data_lines = data_lines.replace("GEXP","./matrix/SRCBIGRIPS")
        data_lines = data_lines.replace("132, 54, 800.0","%lf, %d, %lf"%(Beam.beam_Au,Beam.beam_Q,Beam.beam_MeVu))
        data_lines = data_lines.replace(
"""10000
 800.0, 0, 132, 54
 2
 0.001, 10, 0, 0, 0
 2
 0.001, 10, 0, 0, 0
 1
 1.000,  0, 0, 0, 0""",
"""%d
%lf, 0, %lf, %d
%d
%lf, %lf, 0, 0, 0
%d
%lf, %lf, 0, 0, 0
%d
%lf,  0, 0, 0, 0
"""%(
    ndata,
    Beam.beam_MeVu,Beam.beam_Au,Beam.beam_Q,
    dist_shape,
    Beam.sigmaX_mm/10.,Beam.sigmaA_mrad,
    dist_shape,
    Beam.sigmaY_mm/10.,Beam.sigmaB_mrad,
    dist_shape,
    Beam.sigmaP * (Beam.beam_gamma + 1)/Beam.beam_gamma
)
        )

        data_lines = data_lines.replace(
""" DRIFT
  194.500000""",
""" MATRIX                   'ff' 
 ./matrix/SRCBIGRIPS000.MAT
 %lf, %d, %lf                          
 3, 3                                    
 SAVE #1
 MATRIX                   'ff' 
 ./matrix/SRC000GICO.MAT
 %lf, %d, %lf                          
 3, 3
 SAVE #2
 DRIFT
 194.500000"""%(Beam.beam_Au,Beam.beam_Q,Beam.beam_MeVu,
                Beam.beam_Au,Beam.beam_Q,Beam.beam_MeVu))
        
        data_lines = re.sub(
r""" COLL
 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}
""",
r""" COLL
 3, 0, 0,   \1,   \2,   0
""",data_lines)

#        data_lines = data_lines.replace(r" 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}"," 3, 0, 0,   \1,   \2,   0")
#        data_lines = re.sub(r" 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}"," 3, 0, 0,   \1,   \2,   0",data_lines)


        
        nelement = 4;
        data_lines = re.sub(
  r""" \*----------------------------------
 EXPECTED-VALUES
 SAVE   #           [0-9]
 \*----------------------------------
""","",data_lines)
        
        while 1:
            data_lines_prev = data_lines
            data_lines= re.sub(
r"""COLL
 ([0-9].*)
 MATRIX                 'dipole'
 ./matrix/SRCBIGRIPS([0-9]{3}).MAT
 ([0-9].*)
 3, 3                                    
 COLL
 ([0-9].*)""",
# """ MATRIX                 'dipole'
#  ./matrix/SRCBIGRIPS([0-9]{3}).MAT
#  ([0-9].*)
#  3, 3                                    
#  COLL
#  ([0-9].*)""",
r"""SAVE # %d savepoint before dipole
 COLL
 \1
 SAVE # %d savepoint inside dipole
 MATRIX                 'dipole'
 ./matrix/SRCBIGRIPS\2.MAT
 \3
 3, 3
 COLL
 \4
 SAVE # %d savepoint after dipole"""%(nelement-1,nelement, nelement + 1),data_lines, 1)
            if nelement == 10:
                break            
            nelement += 3

#             if nelement == 7:
#                 data_lines= re.sub(
# r"""COLL
#  ([0-9].*)
#  MATRIX                'quadrupole'
#  ./matrix/SRCBIGRIPS029.MAT
#  ([0-9].*)
#  3, 3                                    
# """,
# r"""SAVE # %d savepoint before QDT12a
#  COLL
#  \1
#  MATRIX                'quadrupole'
#  ./matrix/SRCBIGRIPS029.MAT
#  \2
#  3, 3
#  SAVE # %d savepoint after QDT12b"""%(nelement-1,nelement),data_lines, 1)
#                 nelement += 2
        
        coll_size_list =  re.findall(
r"""COLL
 ([0-9]), 0, 0,\s+([0-9]{1,}\.[0-9]{1,}),\s+([0-9]{1,}\.[0-9]{1,}),\s+0
 """        
        ,data_lines)

        for coll_size in coll_size_list:
            data_lines =  re.sub(
r"""COLL
 ([0-9]), 0, 0,\s+[0-9]{1,}\.[0-9]{1,},\s+[0-9]{1,}\.[0-9]{1,},\s+0
 """,        
r"""COLL
 \1, 0, 0, %lf, %lf, 0.0  
 """%(duct_scale_factor*float(coll_size[1]),duct_scale_factor*float(coll_size[2]))        
            ,data_lines,1)
                 
        if flag_calc_1st_order == 1:
                    data_lines = data_lines.replace("3, 3","1, 1")
        
                 
        print(data_lines)
    with open(file_name_mocadi_out,mode="w",encoding = "utf-8") as f_out:
        f_out.write(data_lines)
        nelement += 2
    return "./rbm-bigrips%s.hbk"%extra_name, nelement        
