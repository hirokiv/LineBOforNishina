import os
import sys
import re
import Ana_Root_Transmission

ndata=10000
Init_Gicosy=0
Init_Mocadi=0

beam_Z=13
beam_A=51
beam_Au=50.936825
beam_MeVu=6.00799
#beam_MeVu=100

sigmaX_mm=2.1/2. 
sigmaA_mrad=2.7/2. 
sigmaY_mm=1.8/2.
sigmaB_mrad=3.5/2. 
sigmaP=0.05 
duct_upstream=3.0
duct_downstream=3.0
flag_calc_1st_order=0
flag_Initial_phase=1

#Dipole_num=[5,8,11,14,15]
Dipole_num=[6]


args = sys.argv
print("# of args = ",len(args))
if len(args) > 2:
    Init_Gicosy = int(args[2])
if len(args) > 3:    
    Init_Mocadi = int(args[3])

if Init_Gicosy == 1:
    os.system('cp ./gicosy_dat/HEBT_GARIS3.dat .')
    os.system('cp HEBT_GARIS3.dat HEBT_GARIS3%s.dat'%args[1])
    os.system('./gicosy.sh HEBT_GARIS3%s.dat'%args[1])

if Init_Mocadi == 1:
    os.system('./gicosy2mocadif HEBT_GARIS3%s_out.dat'%args[1])

    file_name_mocadi     = "GICOSYOUT.in"
    file_name_mocadi_out = "HEBT_GARIS3%s.in"%args[1]
    data_lines=None
        
    with open(file_name_mocadi,encoding = "utf-8") as f_in:
        data_lines = f_in.read()        

        # beam        
        data_lines = data_lines.replace("GEXP","./matrix/GARISIII")
        data_lines = data_lines.replace("132, 54, 800.0","%lf, %d, %lf"%(beam_Au,beam_Z,beam_MeVu))
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
2
%lf, %lf, 0, 0, 0
2
%lf, %lf, 0, 0, 0
2
%lf,  0, 0, 0, 0
"""%(
    ndata,
    beam_MeVu,beam_Au,beam_Z,
    sigmaX_mm/10.,sigmaA_mrad,
    sigmaY_mm/10.,sigmaB_mrad,
    sigmaP
)
        )

        data_lines = re.sub(
r""" DRIFT
   ([0-9].*)
 MATRIX                   'ff' 
 ./matrix/GARISIII([0-9]{3}).MAT
 ([0-9].*)
 3, 3                                    
 COLL
 ([0-9].*)
 MATRIX                 'dipole'
 ./matrix/GARISIII([0-9]{3}).MAT
 [0-9].*
 3, 3                                    
 COLL
 ([0-9].*)
 MATRIX                   'ff' 
 ./matrix/GARISIII([0-9]{3}).MAT
 [0-9].*
 3, 3                                    
 DRIFT
   ([0-9].*)
""",
r""" COLL
 3, 0, 0, 2.95, 2.95, 0
 DRIFT
   \1
 MATRIX                   'ff' 
 ./matrix/GARISIII\2.MAT
 \3
 3, 3                                    
 COLL
 \4
 MATRIX                 'dipole'
 ./matrix/GARISIII\5.MAT
 \3
 3, 3                                    
 COLL
 \6
 MATRIX                   'ff' 
 ./matrix/GARISIII\7.MAT
 \3
 3, 3                                    
 DRIFT
   \8
 COLL
 3, 0, 0, 2.95, 2.95, 0
""",data_lines,2)                            



        if flag_Initial_phase == 1:
            data_lines = data_lines.replace(
""" DRIFT
   49.599998
""",
""" DRIFT
 0.000
MATRIX                   'ff' 
 ./matrix/GARISIII000.MAT
 %lf, %d, %lf                          
 3, 3                                    
 SAVE #1
 DRIFT
 49.599998
"""%(beam_Au,beam_Z,beam_MeVu))

        else:
            data_lines = data_lines.replace(
""" DRIFT
   49.599998
""",
""" DRIFT
 0.000
 SAVE #1
 DRIFT
 49.599998
""")
        # beam duct in DMe2
        data_lines = data_lines.replace(
""" COLL
 4, 0, 0,   2.500,   2.500,   2.500
""",
""" COLL
 1, 0, 0,  20.000,   2.500,   0.000
""")
        
        # beam duct shape
        data_lines = re.sub(
r""" COLL
 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}
""",
r""" COLL
 3, 0, 0,   \1,   \2,   0
""",data_lines)

        data_lines = data_lines.replace(r" 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}"," 3, 0, 0,   \1,   \2,   0")
#        data_lines = re.sub(r" 4, 0, 0,   ([0-9]\.[0-9]{3}),   ([0-9]\.[0-9]{3}),   [0-9]\.[0-9]{3}"," 3, 0, 0,   \1,   \2,   0",data_lines)


        # beam duct in DMe1
        data_lines = data_lines.replace(
""" COLL
 1, 0, 0,  20.000,   5.980, 0
""",
""" COLL
 1, 0, 0,  20.000,   2.500, 0
""")
        
        
        nelement = 3;
        data_lines = re.sub(
  r""" \*----------------------------------
 EXPECTED-VALUES
 SAVE   #           [0-9]
 \*----------------------------------
""","",data_lines)
        
        while 1:
            data_lines_prev = data_lines
            data_lines= re.sub(
r""" MATRIX                'quadrupole'
 ./matrix/GARISIII([0-9]{3}).MAT
 ([0-9].*)
 3, 3                                    
 COLL
 ([0-9].*)
 MATRIX                   'ff' 
""",
r""" MATRIX                'quadrupole'
 ./matrix/GARISIII\1.MAT
 \2
 3, 3                                    
 COLL 
 \3
 SAVE # %d savepoint for quadrupole 
 MATRIX                   'ff' 
"""%(nelement-1)
                ,data_lines,1)
            if data_lines != data_lines_prev:
                nelement += 1
                
            if nelement in Dipole_num:
                 data_lines= re.sub(
r""" MATRIX                 'dipole'
 ./matrix/GARISIII([0-9]{3}).MAT
 ([0-9].*)
 3, 3                                    
 COLL
 ([0-9].*)
 MATRIX                   'ff' 
""",
r""" MATRIX                 'dipole'
 ./matrix/GARISIII\1.MAT
 \2
 3, 3                                    
 COLL
 \3
 SAVE # %d savepoint for dipole
 MATRIX                   'ff' 
"""%(nelement-1),
                     data_lines, 1)
                 nelement += 1
            
            if data_lines == data_lines_prev:
                     break

        if flag_calc_1st_order == 1:
                    data_lines = data_lines.replace("3, 3","1, 1")
        
                 
        print(data_lines)
    with open(file_name_mocadi_out,mode="w",encoding = "utf-8") as f_out:
        f_out.write(data_lines)

    os.system('mocadiR40 HEBT_GARIS3%s.in'%args[1])
    Ana_Root_Transmission.Ana_transmission_GARIS3("./HEBT_GARIS3%s.root"%args[1],11)
    os.system('mv ./HEBT_GARIS3%s.root ./Root/HEBT_GARIS3%s_%dsample_%delement.root'%(args[1],args[1],ndata,nelement))
